from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_login import current_user
from application.auth.models import User
import logging


def generate_token(raw_text):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    return serializer.dumps(raw_text, current_app.config.get('TOKEN_SALT'))


def confirm_token(token, secret, expiration):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    try:
        decoded_secret = serializer.loads(token, max_age=expiration, salt=current_app.config.get('TOKEN_SALT'))
        return decoded_secret == secret
    except Exception as e:
        logging.info(f"Error : {e}")
        return False


def confirm_reset_password_token(token, expiration):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    try:
        decoded_secret = serializer.loads(token, max_age=expiration, salt=current_app.config.get('TOKEN_SALT'))
        return User.query.filter_by(email=decoded_secret).first()
    except Exception as e:
        logging.info(f"Error : {e}")
        return False
