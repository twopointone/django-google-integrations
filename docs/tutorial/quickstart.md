# Quickstart

We will create a test application implementing Google OAuth using django-google-integrations

## Project setup

```
# Create the project directory
mkdir example
cd example

# Create a virtual environment to isolate our package dependencies locally
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install Django and Django REST framework into the virtual environment
pip install django
pip install djangorestframework
pip install django-google-integrations

# Set up a new project with a single application
django-admin startproject example .  # Note the trailing '.' character
cd example
django-admin startapp testapp
cd ..
```

Add `django_google_integrations` app in your INSTALLED_APPS

```
INSTALLED_APPS = [
    ......
    "rest_framework",
    "django_google_integrations",
    "testapp",
]
```

Define your urls.py

```
default_router = routers.DefaultRouter(trailing_slash=False)
default_router.register("api/auth/google", GoogleAuthViewSet, basename="google-auth")
```

Create your models to store user information

```
# models.py
class User(Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    google_id = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(unique=True, db_index=True)
    date_joined = models.DateTimeField(default=timezone.now)
```

Create Serializers to handle response

```
# serializers.py
from rest_framework import serializers

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "google_id",
            "date_joined"
        ]

```

Create `google_response_handler.py` file in your `testapp` and override `GoogleResponseHandler` class to handle incoming response from google

```
from example.testapp.serializers import AuthUserSerializer
from django_google_integrations.services import GoogleResponseHandler
from example.testapp.services import create_user_account, get_user_by_email

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

The project layout should look like:

```
$ pwd
<some path>/example

$ find .
.
./testapp
./testapp/migrations
./testapp/migrations/__init__.py
./testapp/migrations/0001_initial.py
./testapp/models.py
./testapp/serializers.py
./testapp/__init__.py
./testapp/apps.py
./testapp/admin.py
./testapp/google_response_handler.py
./example
./example/__init__.py
./example/settings.py
./example/urls.py
./example/wsgi.py
./manage.py
```

Define Google Config in settings.py file, you can generate these values from [google cloud console](https://console.cloud.google.com/iam-admin/iam)

```
# django-google-integrations config
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

### Testing app

Run following command to create your migration file

```
python manage.py makemigrations
python manage.py migrate
```

Run django server

```  
python manage.py runserver
```

Now you can access your urls from shell using [httpie](https://httpie.io/) or [Postman](https://www.postman.com/)

### Generate Authorization URL

```
http GET localhost:8000/api/auth/google/auth-url
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Language: en
Content-Length: 537
Content-Type: application/json; charset=utf-8
Request_id: 94494c0acc584dc3b20cbd29763fd341
Vary: Accept, Accept-Language, Cookie, Origin
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block

{
    "authorization_url": "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=243243243243-o91vlam4808du0454jsal4g.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fgoogle%2Fauth%2Fcallback&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&state=TYBKHoujnjkho3245lnl&code_challenge=Z4kfoAWat4XjpVpajEMKV0BWhV-63QFpK0v8sPcbH6w&code_challenge_method=S256&access_type=offline&include_granted_scopes=true"
}
```

`authorization_url` will redirect to google signin page
After successful login you will be redirected to your `redirect url` with some query parameters
```
http://localhost:3000/google/auth/callback?state={state}&code={auth_code}&scope={scope}
```

### Authorize Tokens

```
POST /api/auth/google/authorize
```

```
{
    "state":"NFvYBYlgIfp91JxPOmGuG1N4ACElVe",
    "auth_code":"4/0AX4XfWjwvCFOwNKHaasZ9dgSX4WM8QPwW1xU4miWm_dNxRpYdgS_FHCpOOTG7SKN7Aw-7Q"
}
```

**Response**

Response can be generated by overriding `generate_response_json` method of `GoogleResponseHandler` class

```
def generate_response_json(self, user, extra_context):
        response = AuthUserSerializer(user)
        return response.data
```
