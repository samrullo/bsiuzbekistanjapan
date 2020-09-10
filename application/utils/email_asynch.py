from flask_mail import Message
from application import mail
from flask import current_app
from application import create_app
from threading import Thread


def send_async_email(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, sender, recipient, plain_text_body, html_body):
    message = Message(subject=subject, recipients=[recipient], sender=sender, body=plain_text_body, html=html_body)
    another_app=create_app('development')
    thr = Thread(target=send_async_email, args=[another_app, message])
    thr.start()
    return thr
