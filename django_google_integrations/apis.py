# Third Party Stuff
from django.utils.encoding import smart_str
from oauthlib.oauth2 import InvalidGrantError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# Django Google Integrations Stuff
from django_google_integrations.exceptions import GoogleAuthException
from django_google_integrations.serializers import (
    GoogleAuthSerializer,
    IOSGoogleAuthSerializer,
)
from django_google_integrations.services import GoogleAuth
from django_google_integrations.settings import google_api_settings


class GoogleAuthViewSet(viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    response_handler_class = google_api_settings.RESPONSE_HANDLER_CLASS
    serializer_class = GoogleAuthSerializer
    ios_token_serializer = IOSGoogleAuthSerializer

    @action(methods=["POST"], detail=False)
    def authorize(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            response_handler = self.response_handler_class()
            google_auth = GoogleAuth()
            user, extra_context = google_auth.authorize_user(
                request=request,
                state=serializer.validated_data["state"],
                auth_code=serializer.validated_data["auth_code"],
                code_verifier=serializer.data["code_verifier"],
                response_handler=response_handler,
            )
            response_dict = response_handler.generate_response_json(
                request, user, extra_context
            )
            return Response(response_dict, status=HTTP_200_OK)

        except InvalidGrantError as e:
            raise GoogleAuthException(smart_str(e))

    @action(methods=["GET"], detail=False, url_path="auth-url")
    def auth_url(self, request, *args, **kwargs):
        try:
            google_auth = GoogleAuth()
            auth_url = google_auth.get_authorization_url()
            return Response({"authorization_url": auth_url}, status=HTTP_200_OK)
        except InvalidGrantError as e:
            raise GoogleAuthException(smart_str(e))

    @action(methods=["POST"], detail=False, url_path="authorize/ios")
    def authorize_ios(self, request, *args, **kwargs):
        serializer = self.ios_token_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        response_handler = self.response_handler_class()
        try:
            google_auth = GoogleAuth()
            user, extra_context = google_auth.authorize_ios_token(
                request, token, response_handler
            )
            response_dict = response_handler.generate_response_json(user, extra_context)
            return Response(response_dict, status=HTTP_200_OK)

        except InvalidGrantError as e:
            raise GoogleAuthException(smart_str(e))
