# Google Integrations Test App

In a python virtualenv run:

```
pip install -r requirements.txt
```

Configure Google Config in your settings file

```
GOOGLE_CONFIG = {
    "RESPONSE_HANDLER_CLASS": "example.testapp.google_response_handler.GoogleSigninResponseHandler",
    "CLIENT_CONFIG_JSON": "",
    "CLIENT_ID": "",
    "CLIENT_SECRET": "",
    "CONTACT_SCOPE": "",
    "SERVICE_ACCOUNT_SCOPES": [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    "REDIRECT_URI": "",
}
```

To launch a functional server:

```
$ ./manage.py migrate
$ ./manage.py createsuperuser
```

And run the server:

```
$ ./manage.py runserver
```
