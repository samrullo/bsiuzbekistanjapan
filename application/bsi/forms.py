from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from application.bsi.models import SendingDate
from flask_babel import lazy_gettext as _


class BSIPostWeightForm(FlaskForm):
    weight = FloatField(_("Weight (in kg)"), validators=[DataRequired()])
    submit = SubmitField(_("Submit"))


class SendingDateForm(FlaskForm):
    sending_date = DateField(_("Enter sending date"), validators=[DataRequired()],
                             render_kw={"placeholder": "YYYY-MM-DD"})
    note = StringField(_("Enter note"))
    submit = SubmitField(_("Submit"))

    def validate_sending_date(self,field):
        if SendingDate.query.filter_by(sending_date=field.data).first():
            raise ValidationError(_("This sending date already exists"))
