import os
from ..auth import auth_bp
from oauthlib.oauth2 import WebApplicationClient
from ..utils.google_login_utils import get_google_provider_cfg
from application import db
from flask_login import login_required, current_user
from .models import User
from ..auth.forms import RegisterForm
from flask import request, redirect, current_app, flash, g
from flask_babel import lazy_gettext as _
from flask_login import login_user
from ..utils.custom_url_for import url_for
import datetime

import requests
import json


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
            user = User(email=users_email, name=users_name, password=os.urandom(23),is_confirmed=True,
                        is_google_account=True,
                        confirmed_on=datetime.datetime.utcnow())
            db.session.add(user)
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
