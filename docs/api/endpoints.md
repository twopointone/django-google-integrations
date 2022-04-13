# Google OAuth 2.0

## Get Authorization URL

- Authorization URL is used to redirect to Google's Authorization Server to request consent from resource owner.
- `state` query parameter can be passed as a JSON object, response will contain the same object along with state `identifier`.

    ```
    GET {BASE_URL}/auth-url
    ```


    **Request**

    ```
    GET {url-prefix}/auth-url?state={"redirect_to": "profile_page"}
    ```

    **Response**

    `status: 200 OK`

    ```json
    {
        "authorization_url": "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=<CLIENT_ID>&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fapi%2Fauth%2Fcallback&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&state=%7B%22identifier%22%3A+%22QOFXM02OEAQT7C10UPS9EP71BLALBF%22%2C+%22redirect_to%22%3A+%22profile_page%22%7D&code_challenge=Maol74w--9Um8Yp2AyqJtsajQBtkhTN7V4ZRlsN1qQI&code_challenge_method=S256&access_type=offline&include_granted_scopes=true"
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

    **Request**

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


## Authorize iOS Token

- Verifies an ID Token issued by Google's OAuth 2.0 authorization server and fetch user details from decoded token.

    ```
    POST {BASE_URL}/authorize/ios
    ```

    **Request**

    ```json
    {
      "token": "xyz123"
    }
    ```

    **Response**
    ```
    "Response needs to be defined by overriding the GoogleResponseHandler class""
    ```
