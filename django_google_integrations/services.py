# Standard Library
import json
import logging

# Third Party Stuff
import google_auth_oauthlib.helpers
from django.utils import timezone
from django.utils.crypto import get_random_string
from google.auth.transport import requests
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

# Django Google Integrations Stuff
from django_google_integrations.models import (
    GoogleAuthIntermediateState,
    UserGoogleAuthCredential,
)
from django_google_integrations.settings import google_api_settings

logger = logging.getLogger(__name__)


class GoogleResponseHandler:
    def fetch_google_user_details(self, request, flow):
        session = flow.authorized_session()
        google_user_data = session.get(
            "https://www.googleapis.com/userinfo/v2/me"
        ).json()
        return self.handle_fetch_or_create_user(request, flow, google_user_data)

    def handle_fetch_or_create_user(self, request, flow, google_user_data):
        """
        params:
            flow: GoogleAuthFlow
            google_user_data: dict of responses after successful authentication
        return:
            user: user object
            extra_context: dict
        """
        raise NotImplementedError()

    def handle_scopes(self):
        return

    def generate_response_json(self, request, user, extra_context):
        raise NotImplementedError()


class GoogleAuthFlow(Flow):
    # Overridden to resolve issue: https://github.com/googleapis/google-auth-library-python-oauthlib/issues/45
    @classmethod
    def from_client_config(cls, client_config, scopes, **kwargs):
        """Creates a :class:`requests_oauthlib.OAuth2Session` from client
        configuration loaded from a Google-format client secrets file.

        Args:
            client_config (Mapping[str, Any]): The client
                configuration in the Google `client secrets`_ format.
            scopes (Sequence[str]): The list of scopes to request during the
                flow.
            kwargs: Any additional parameters passed to
                :class:`requests_oauthlib.OAuth2Session`

        Returns:
            Flow: The constructed Flow instance.

        Raises:
            ValueError: If the client configuration is not in the correct
                format.

        .. _client secrets:
            https://developers.google.com/api-client-library/python/guide
            /aaa_client_secrets
        """
        if "web" in client_config:
            client_type = "web"
        elif "installed" in client_config:
            client_type = "installed"
        else:
            raise ValueError("Client secrets must be for a web or installed app.")

        code_verifier = kwargs.pop("code_verifier", None)
        (
            session,
            client_config,
        ) = google_auth_oauthlib.helpers.session_from_client_config(
            client_config, scopes, **kwargs
        )

        redirect_uri = kwargs.get("redirect_uri", None)
        return cls(session, client_type, client_config, redirect_uri, code_verifier)


class GoogleAuth(object):
    config = google_api_settings

    def __init__(self):
        self._credentials_obj = None

    def _get_authorization_url(self, flow, code_verifier, **kwargs):
        # Generate URL for request to Google's OAuth 2.0 server.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type="offline",
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes="true",
        )
        return authorization_url, state

    def __get_flow(self, **kwargs):
        code_verifier = kwargs.pop("code_verifier", "") or get_random_string(length=43)
        client_config = json.loads(self.config.CLIENT_CONFIG_JSON)
        flow = GoogleAuthFlow.from_client_config(
            client_config,
            scopes=self.config.SERVICE_ACCOUNT_SCOPES,
            code_verifier=code_verifier,
            **kwargs
        )
        flow.redirect_uri = self.config.REDIRECT_URI
        return flow, code_verifier

    def __save_intermediate_state(self, state, code_verifier):
        return GoogleAuthIntermediateState.objects.create(
            state=state, code_verifier=code_verifier
        )

    def __save_user_auth_credentials(self, credentials, user):
        timezone_aware_expiry = timezone.make_aware(credentials.expiry)
        defaults = {
            "access_token": credentials.token,
            "expires_at": timezone_aware_expiry,
        }
        if credentials.refresh_token:
            defaults["refresh_token"] = credentials.refresh_token
        return UserGoogleAuthCredential.objects.update_or_create(
            user=user, defaults=defaults
        )

    def authorize_user(
        self, request, state, auth_code, code_verifier, response_handler
    ):
        flow, _ = self.__get_flow(state=state, code_verifier=code_verifier)
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        self._credentials_obj = credentials
        user, extra_context = response_handler.fetch_google_user_details(request, flow)
        self.__save_user_auth_credentials(credentials, user)
        return user, extra_context

    def get_authorization_url(self):
        flow, code_verifier = self.__get_flow()
        authorization_url, state = self._get_authorization_url(flow, code_verifier)
        self.__save_intermediate_state(state, code_verifier)
        return authorization_url

    def __get_new_auth_credentials(self, refresh_token):
        flow, _ = self.__get_flow()
        flow.oauth2session.refresh_token(
            token_url=flow.client_config["token_uri"],
            client_secret=flow.client_config["client_secret"],
            client_id=flow.client_config["client_id"],
            refresh_token=refresh_token,
        )
        return flow.credentials

    def refresh_user_access_token(self, user):
        user_auth_credentials = UserGoogleAuthCredential.objects.filter(
            user=user
        ).first()
        if user_auth_credentials:
            credentials = self.__get_new_auth_credentials(
                user_auth_credentials.refresh_token
            )
            self._credentials_obj = credentials
            self.__save_user_auth_credentials(credentials, user)
            return user_auth_credentials

    def get_oauth_credentials_obj(self, user):
        if not getattr(self, "_credentials_obj", None):
            flow, _ = self.__get_flow()
            user_auth_credentials = UserGoogleAuthCredential.objects.filter(
                user=user
            ).first()
            if user_auth_credentials:
                self._credentials_obj = Credentials(
                    token=user_auth_credentials.access_token,
                    refresh_token=user_auth_credentials.refresh_token,
                    token_uri=flow.client_config["token_uri"],
                    client_id=flow.client_config["client_id"],
                    client_secret=flow.client_config["client_secret"],
                    scopes=flow.oauth2session.scope,
                )
        return getattr(self, "_credentials_obj", None)

    def authorize_ios_token(self, request, token, response_handler):
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), self.config.GOOGLE_IOS_CLIENT_ID
        )
        google_user_data = {
            "id": id_info["sub"],
            "email": id_info["email"],
            "given_name": id_info.get("given_name", ""),
            "family_name": id_info.get("family_name", ""),
            "picture": id_info.get("picture", None),
        }
        user, extra_context = response_handler.handle_fetch_or_create_user(
            request=request, flow=None, google_user_data=google_user_data
        )
        return user, extra_context
