from flask_mail import Message
from googleapiclient.discovery import build
from flask import current_app
from .gmail_api_server_side_authorization import get_stored_credentials
from apiclient import errors
import base64
from email.mime.text import MIMEText


def create_message(sender, to, subject, message_text, cc=None):
    """
    MIMEText を base64 エンコードする
    """
    enc = "utf-8"
    message = MIMEText(message_text.encode(enc), 'html', _charset=enc)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    if cc:
        message["Cc"] = cc
    encode_message = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": encode_message.decode()}


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
