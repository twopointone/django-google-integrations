# Django Google Integrations Documentation

__Version:__ "0.0.1"

Django Google Integrations is a package that allows integrating Google OAuth into your Django application. It is build as a thin wrapper around the [google-auth-oauthlib](https://github.com/googleapis/google-auth-library-python-oauthlib).
You can view the full documentation at https://PrimedigitalGlobal.github.io/django-google-integrations/

## Features

- Provides following APIs:
  - Authorization URL API:
    - It generates google `authorization-url` which redirects user to Google's Authorization Server to request consent from resource owner.
  - Authorize Web API:
    - Exchange authorization code for access token.
    - Talk to resource server with access token and fetch user's profile information.
  - Authorize IOS Token API:
    - Verifies an ID Token issued by Google's OAuth 2.0 authorization server.
    - Fetch user details from decoded token.

## API

- [Overview](api/overview.md)
- [Endpoints](api/endpoints.md)

**NOTE:** This documentation changes frequently, checkout the [changelog](api/changelog.md) for detailed breaking changes and features added.

Write your documentation using **Markdown** in `docs/` folder. Need help? Read mkdocs [documentation][mkdocs].

[mkdocs]: http://www.mkdocs.org/user-guide/writing-your-docs/
