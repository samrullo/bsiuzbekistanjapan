import logging
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _
from wtforms import StringField, PasswordField, DateField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from application import moment
import datetime

class PostWeightForm(FlaskForm):
    sent_date = DateField(_("Sent date"), validators=[DataRequired()],render_kw={"value":datetime.date.today()})
    weight = FloatField(_("Weight (in kg)"), validators=[DataRequired()])
    submit = SubmitField(_("Submit"))


class BSIPostWeightForm(FlaskForm):
    weight = FloatField(_("Weight (in kg)"), validators=[DataRequired()])
    submit = SubmitField(_("Submit"))
