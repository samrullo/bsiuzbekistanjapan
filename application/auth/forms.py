import logging
from flask_wtf import FlaskForm
from flask_login import current_user
from flask_babel import lazy_gettext as _
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from .models import User
from flask import current_app


class LoginForm(FlaskForm):
    email = StringField(_("Email"), validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(_("Password"), validators=[DataRequired()])
    remember = BooleanField(_("Keep me logged in"))
    submit = SubmitField(_("Log In"))


class RegisterForm(FlaskForm):
    email = StringField(_("Email"), validators=[DataRequired(), Length(1, 64), Email()])
    name = StringField(_("Name"), validators=[DataRequired()], render_kw={"placeholder": _("<Last name> <First name>")})
    phone = StringField(_("Phone"), render_kw={"placeholder": _("080-1234-1234")})
    address = StringField(_("Address"))
    password = PasswordField(_("Password"),
                             validators=[DataRequired(), EqualTo("confirm_password", message="Passwords must match")])
    confirm_password = PasswordField(_("Confirm Password"), validators=[DataRequired()])
    submit = SubmitField(_("Register"))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_("Email already exists"))


class EditProfileForm(FlaskForm):
    name = StringField(_("Name"), validators=[DataRequired()], render_kw={"placeholder": _("<Last name> <First name>")})
    phone = StringField(_("Phone"), render_kw={"placeholder": _("080-1234-1234")})
    address = StringField(_("Address"))
    submit = SubmitField(_("Save"))

class ResetPasswordSendLinkForm(FlaskForm):
    email = StringField(_("Please enter your email"), validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField(_("Send password reset link"))

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError(
                _("This email doesn't exist in our system. Please enter the email you registered with."))


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(_("Enter the new password"), validators=[DataRequired(), EqualTo('confirm_password',
                                                                                                  message=_(
                                                                                                      "Passwords don't match"))])
    confirm_password = PasswordField(_("Confirm the password"), validators=[DataRequired()])
    submit = SubmitField(_("Save new password"))
