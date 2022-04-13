# Django Google Integrations Documentation

__Version:__ 0.0.2

Django Google Integrations is a package that allows integrating Google OAuth 2.0 into your Django application. It is build as a thin wrapper around the [google-auth-oauthlib](https://github.com/googleapis/google-auth-library-python-oauthlib).

## Features

- Provides following APIs:
    - [**Authorization URL API**](api/endpoints/#get-authorization-url)
        - It generates google `authorization-url` used to redirect to Google's Authorization Server to request consent from resource owner.
    - [**Authorize Web API**](api/endpoints/#get-user-information)
        - Exchange authorization code for access token.
        - Talk to resource server with access token and fetch user's profile information.
    - [**Authorize IOS Token API**](api/endpoints/#authorize-ios-token)
        - Verifies an ID Token issued by Google's OAuth 2.0 authorization server.
        - Fetch user details from decoded token.

**NOTE:** This documentation changes frequently, checkout the [changelog](changelog.md) for detailed breaking changes and features added.

Write your documentation using **Markdown** in `docs/` folder. Need help? Read mkdocs [documentation][mkdocs].

[mkdocs]: http://www.mkdocs.org/user-guide/writing-your-docs/
