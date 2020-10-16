import logging
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _
from wtforms import StringField, PasswordField, DateField, FloatField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from application import moment
import datetime


class PostWeightForm(FlaskForm):
    # countries = [(country.id, country.country_name) for country in Country.query.all()]
    # represented_individuals = [(represented_individual.id, represented_individual.name) for represented_individual in
    #                            RepresentedIndividual.query.all()]
    # recipients = [(recipient.id, recipient.name) for recipient in
    #               Recipient.query.all()]
    from_country = SelectField(_("From country"), coerce=int, validate_choice=False)
    to_country = SelectField(_("To country"), coerce=int, validate_choice=False)
    represented_individual = SelectField(_("Represented individual"), coerce=int, validate_choice=False)
    recipient = SelectField(_("Recipient"), coerce=int, validate_choice=False)
    sent_date = DateField(_("Sent date"), validators=[DataRequired()], render_kw={"value": datetime.date.today()})
    weight = FloatField(_("Weight (in kg)"), validators=[DataRequired()])
    submit = SubmitField(_("Submit"))


class RepresentedIndividualRecipientForm(FlaskForm):
    name = StringField(_("Name"), validators=[DataRequired()], render_kw={"placeholder": _("<Last name> <First name>")})
    email = StringField(_("Email"), validators=[DataRequired(), Length(1, 64), Email()])
    phone = StringField(_("Phone"))
    telegram_username = StringField(_("Telegram username"))
    address = StringField(_("Address"))
    submit = SubmitField(_("Register"))
