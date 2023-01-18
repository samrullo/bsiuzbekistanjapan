# Authenticating users with their Google accounts

Authenticating users with Google Oauth2.0 is straightforward.
First you will need to create Oauth2.0 credentials from [Google Cloud Console](https://console.cloud.google.com/apis/dashboard?project=ideliver-374910)
And remember that before you can create Oauth2.0 credentials you will have to first create a project.

Once you have created a project and navigate to *API and Services* > *Credentials*
you can start creating new credentials.

In this application's case I chose *web application* as application type
and then provided following values for important Attributes

- Authorized Javascript origins : https://localhost:5000
- Authorized redirect uris : https://localhost:5000/uz/google_login/callback, https://localhost:5000/en/google_login/callback

After filling in above attributes you will have your credential in place.
We will grab "Client id" and "Client secret" and specify them to following configs

- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET

# How does it work

When user presses "Login with Google" button which has the url of "/<lang>/google_login", the app creates google *client* object by passing *GOOGLE_CLIENT_ID*.



Using *client* object we prepare *request_uri* to which we eventually redirect the user for authorization.
When preparing this *request_uri* we specify 
- authorization_endpoint("https://accounts.google.com/.well-known/openid-configuration")
- redirect_uri : URI to which Google will send authorization code
- scope : a list of strings that specify what Google account data this application can access. Ex : ["openid", "email", "profile"]


```python
@auth_bp.route("/<lang>/google_login")
def google_login():
    client = WebApplicationClient(current_app.config.get('GOOGLE_CLIENT_ID'))
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)
```

In *redirect_uri* view function we receive authorization code.
As a next step we obtain *tokens* by preparing request to send to tokens endpoint.
After getting tokens, we add tokens to *client* object, which will give us 
uri, headers, body
And we use that to finally get user Google account info, confirm that user has validated account and finally register the user into database, by setting *is_google_account* flag of *users* table to True. 

```python
@auth_bp.route("/<lang>/google_login/callback")
def callback():
    client = WebApplicationClient(current_app.config.get('GOOGLE_CLIENT_ID'))
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config.get('GOOGLE_CLIENT_ID'), current_app.config.get('GOOGLE_CLIENT_SECRET')),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]

        user_usual_account = User.query.filter_by(email=users_email, is_google_account=False).first()
        if user_usual_account:
            flash(_("Seems like %(email)s is registered via usual route. Please login using your password",
                    email=users_email), "danger")
            return redirect(url_for('auth_bp.login'))

        user = User.query.filter_by(email=users_email, is_google_account=True).first()
        if not user or not user.is_confirmed:
            user = User(email=users_email, name=users_name, password=str(os.urandom(23)), is_confirmed=True,
                        is_google_account=True,
                        confirmed_on=datetime.datetime.utcnow())
            db.session.add(user)
            db.session.commit()
            user.set_username()
            # add the user as a first represented individual
            represented_individual = RepresentedIndividual(name=user.name,
                                                           email=user.email,
                                                           phone=user.phone,
                                                           telegram_username=user.telegram_username,
                                                           address=user.address,
                                                           user_id=user.id)
            db.session.add(represented_individual)
            db.session.commit()

            flash(_("Successfully registered %(name)s. Please consider to edit your profile later",
                    name=user.name), "success")
            login_user(user)
            return redirect(url_for('auth_bp.edit_profile'))
        login_user(user)
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('main_bp.home')
        return redirect(next)
    else:
        return "User email not available or not verified by Google.", 400
```

