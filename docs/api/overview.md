# Django Google Integrations

It provides three endpoints:

- {base-url}/auth-url: To generate Google Authorization URL.
- {base-url}/authorize: To fetch user data from Google server.
- {base-url}/ios/authorize: Verifies an ID Token issued by Google's OAuth 2.0 authorization server and fetch user details from decoded token.

## Dependencies

- Python >= 3.6
- Django >= 2.2.17
- djangorestframework >= 3.10.2
- google-api-python-client >= 2.9.0
- google-auth-httplib2 >= 0.1.0
- google-auth-oauthlib >= 0.4.1

## Setup

You can install the library directly from pypi using pip:

```
$ pip install django-google-integrations
```

Edit your settings.py file:

```
INSTALLED_APPS = (
        ...
        "django_google_integrations"
)

# Django Google Integrations Config
GOOGLE_CONFIG = {
    "CLIENT_CONFIG_JSON": "[Google Client Config Json]",
    "CLIENT_ID": "[Google Client ID]",
    "CLIENT_SECRET": "[Google Client Secret]",
    "SERVICE_ACCOUNT_SCOPES": [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
    "REDIRECT_URI": "http://localhost:3000/google/auth/callback",
    "RESPONSE_HANDLER_CLASS": "example.testapp.google_response_handler.GoogleSigninResponseHandler",
}
```

Create Response Handler Class and update path in `GOOGLE_CONFIG`

```
from django_google_integrations.services import GoogleResponseHandler

class GoogleSigninResponseHandler(GoogleResponseHandler):
    def handle_fetch_or_create_user(self, flow, google_user_data):
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

    def generate_response_json(self, user, extra_context):
        response = AuthUserSerializer(user)
        return response.data
```

NOTE:

- `AuthUserSerializer` used in above ref. could be created as per app's functionality and contain fields which needs to be sent in response of authorization.
- Following service methods are used in above code ref. which could be created as per app's functionality:
  - `get_user_by_email`
  - `create_user_account`

Update URLs

```
from django_google_integrations.apis import GoogleAuthViewSet

default_router = routers.DefaultRouter(trailing_slash=False)
default_router.register("auth/google", GoogleAuthViewSet, basename="google-auth")
```
