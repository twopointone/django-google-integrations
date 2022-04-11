# Third Party Stuff
from django_google_integrations.services import GoogleResponseHandler
from testapp.serializers import AuthUserSerializer
from testapp.services import create_user_account, get_user_by_email


class GoogleAuthResponseHandler(GoogleResponseHandler):
    def handle_fetch_or_create_user(self, request, flow, google_user_data):
        email = google_user_data.get("email", None)
        user = get_user_by_email(email)
        is_created = False
        if not user:
            user_dict = {
                "first_name": google_user_data.get("given_name", ""),
                "last_name": google_user_data.get("family_name", ""),
                "password": None,
            }
            user = create_user_account(email, **user_dict)
            is_created = True

        extra_context = {"is_created": is_created}
        return user, extra_context

    def generate_response_json(self, request, user, extra_context):
        response = AuthUserSerializer(user)
        return response.data
