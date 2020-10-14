from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_babel import lazy_gettext as _


class GmailAPIForm(FlaskForm):
    email = StringField(_("Email"), render_kw={"class": "form-control"})
    subject = StringField(_("Subject"), render_kw={"class": "form-control"})
    body = TextAreaField(_("Message"), render_kw={"class": "form-control"})
    submit = SubmitField(_("Submit"), render_kw={"class": "btn btn-lg btn-dark"})
