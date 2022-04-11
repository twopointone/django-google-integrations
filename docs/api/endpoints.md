[TOC]

# Google OAuth

## Get Authorization URL

- Authorization URL is used to redirect user to Google's Authorization Server to request consent from resource owner.

```
GET {BASE_URL}/auth-url
```

**Response**

`status: 200 OK`

```json
{
    "authorization_url": "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=<client_id>&redirect_uri=<redirect_uri>&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&state=<state>&code_challenge=uarq2qP_100OjqAt-vFcFsNQbrz3TRxgxgy2j2Jcta4&code_challenge_method=S256&access_type=offline&include_granted_scopes=true"
}
```


## Get user information

- Exchange authorization code for access token and talk to resource server with access token and fetch user's profile information.

Note:

- After successful authorization, the callback will have the authorization code(i.e code) and state.
- We can fetch `state` and `code` from redirect URI query parameters and pass those values to authorize api.

```
POST {BASE_URL}/authorize
```

**Request body:**

```json
{
    "state":"NFvYBYlgIfp91JxPOmGuG1N4ACElVe",
    "auth_code":"4/0AX4XfWjwvCFOwNKHaasZ9dgSX4WM8QPwW1xU4miWm_dNxRpYdgS_FHCpOOTG7SKN7Aw-7Q"
}
```

**Response**

`status: 200 OK`

```
Response needs to be defined by overriding the GoogleResponseHandler class
```


### Authorize iOS Token

- Verifies an ID Token issued by Google's OAuth 2.0 authorization server and fetch user details from decoded token.

```
POST {BASE_URL}/authorize/ios
```

```json
{
  "token": "xyz123"
}
```

**Response**
```
"Response needs to be defined by overriding the GoogleResponseHandler class""
```
