import logging
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _
from wtforms import StringField, PasswordField, DateField, FloatField, IntegerField, BooleanField, SelectField, \
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from application import moment
import datetime
from flask_wtf.file import FileField, FileAllowed
from application import images
from .models import PostTrackingStatus


class PostWeightForm(FlaskForm):
    from_country = SelectField(_("From country"), coerce=int, validate_choice=False)
    to_country = SelectField(_("To country"), coerce=int, validate_choice=False)
    represented_individual = SelectField(
        _("Represented individual (to add new represented individual use the menu above)"), coerce=int,
        validate_choice=False)
    recipient = SelectField(_("Recipient (to add a new recipient use the menu above)"), coerce=int,
                            validate_choice=False)
    sent_date = DateField(_("Sent date"), validators=[DataRequired()], render_kw={"value": datetime.date.today()})
    weight = FloatField(_("Weight (in kg)"), validators=[DataRequired()])
    submit = SubmitField(_("Submit"))


class PostWeightContentForm(FlaskForm):
    name = StringField(_("Content name"), validators=[DataRequired()])
    price = FloatField(_("Price"), validators=[DataRequired()])
    quantity = IntegerField(_("Quantity"), validators=[DataRequired()])
    content_image = FileField(_("Content image"), validators=[
        FileAllowed(images, _('Images only are allowed (optional) (.jpg, .jpe, .jpeg, .png, .gif, .svg, and .bmp)!'))])
    submit = SubmitField(_("Submit"))


class PostTrackingStatusForm(FlaskForm):
    tracking_status = SelectField(_("Tracking status"), choices=[
        (PostTrackingStatus.AWAIT_STATUS, PostTrackingStatus.get_status_description(PostTrackingStatus.AWAIT_STATUS)),
        (PostTrackingStatus.ARRIVED_IN_BSI_OFFICE,
         PostTrackingStatus.get_status_description(PostTrackingStatus.ARRIVED_IN_BSI_OFFICE)),
        (PostTrackingStatus.ON_THE_WAY, PostTrackingStatus.get_status_description(PostTrackingStatus.ON_THE_WAY)),
        (PostTrackingStatus.ARRIVED_IN_DESTINATION,
         PostTrackingStatus.get_status_description(PostTrackingStatus.ARRIVED_IN_DESTINATION)),
        (PostTrackingStatus.DELIVERED, PostTrackingStatus.get_status_description(PostTrackingStatus.DELIVERED))
    ],coerce=int)
    submit = SubmitField(_("Submit"))


class RepresentedIndividualRecipientForm(FlaskForm):
    name = StringField(_("Name"), validators=[DataRequired()], render_kw={"placeholder": _("<Last name> <First name>")})
    email = StringField(_("Email"), validators=[DataRequired(), Length(1, 64), Email()])
    phone = StringField(_("Phone"))
    telegram_username = StringField(_("Telegram username"))
    address = StringField(_("Address"))
    submit = SubmitField(_("Register"))
