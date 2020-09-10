from application import mail
from flask_mail import Message


def send_mail(subject, sender, recipient, plain_text_body, html_body):
    message = Message(subject=subject, recipients=[recipient], sender=sender, body=plain_text_body, html=html_body)
    mail.send(message)

