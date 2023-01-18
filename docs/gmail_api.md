# Use GMAIL API to send emails
First you will have to enable GMAIL API in Google Cloud Console
You can create new credentials as we did in [google_auth](google_oauth.md)

When you specify *localhost* as Javascript origins or redirect uris, Google will treat your application as in Test or Development mode only.

Which means you will have to explicitly add *tester* accounts allowed to use Gmail API through your application.

You can add *tester* accounts by navigating to *Oauth Consent Screen*

# How does it work

If you look at *send_mail* function code, you will find out that sending email with Gmail API is quite straightforward.

- We load *credentials* stored as pickle file. *credentials* is ```oauth2client.client.OAuth2Credentials``` object with attributes like ```access_token```, ```refresh_token``` which are used as equivalents of API token.
- We use *build* function to get *service* object. We pass API name which is gmail, API version "v1" and credentials to *build* function
- We use *service* object to send email with ```service.users().messages().send(userId="me", body=message).execute()```

```python
def send_mail(subject, sender, recipient, plain_text_body, html_body):
    message = create_message(sender, recipient, subject, html_body)
    try:
        creds = get_stored_credentials()
        service = build("gmail", "v1", credentials=creds, cache_discovery=False)
        sent_message = (
            service.users().messages().send(userId="me", body=message).execute()
        )
        current_app.logger.info("Message Id: %s" % sent_message["id"])
        return None
    except errors.HttpError as error:
        current_app.logger.info("An error occurred: %s" % error)
        raise error
```

# How do we update credentials

As the name suggests ```refresh_token``` expires after some time (maybe a month?)
So we prepared ```view```s to update credentials.
In ```gmail_login``` view function, we obtain *authorization_url* and redirect the user to it. We obtain *authorization_url* using ```flow_from_clientsecrets``` function of ```oauth2client.client```. ```flow_from_clientsecrets``` returns ```flow``` object. We use this object's ```step1_get_authorize_url``` method to eventually obtain authorization url.

Once we authorize our callback redirect_uri receives authorization code.
We then use it to update refresh_token and update credentials.

```python
def get_credentials(authorization_code, state):
    """Retrieve credentials using the provided authorization code.

    This function exchanges the authorization code for an access token and queries
    the UserInfo API to retrieve the user's e-mail address.
    If a refresh token has been retrieved along with an access token, it is stored
    in the application database using the user's e-mail address as key.
    If no refresh token has been retrieved, the function checks in the application
    database for one and returns it if found or raises a NoRefreshTokenException
    with the authorization URL to redirect the user to.

    Args:
      authorization_code: Authorization code to use to retrieve an access token.
      state: State to set to the authorization URL in case of error.
    Returns:
      oauth2client.client.OAuth2Credentials instance containing an access and
      refresh token.
    Raises:
      CodeExchangeError: Could not exchange the authorization code.
      NoRefreshTokenException: No refresh token could be retrieved from the
                               available sources.
    """
    email_address = ""
    try:
        credentials = exchange_code(authorization_code)
        current_app.logger.info(f"credentials : {credentials.to_json()}")
        user_info = get_user_info(credentials)
        current_app.logger.info(f"user_info : {user_info}")
        email_address = user_info.get('email')
        if credentials.refresh_token is not None:
            store_credentials(credentials)
            return credentials
        else:
            credentials = get_stored_credentials()
            if credentials and credentials.refresh_token is not None:
                return credentials
    except CodeExchangeException as error:
        logging.error('An error occurred during code exchange.')
        # Drive apps should try to retrieve the user and credentials for the current
        # session.
        # If none is available, redirect the user to the authorization URL.
        error.authorization_url = get_authorization_url(email_address, state)
        raise error
    # No refresh token has been retrieved.
    authorization_url = get_authorization_url(email_address, state)
    raise NoRefreshTokenException(authorization_url)
```
