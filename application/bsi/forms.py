from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

class BSIPostWeightForm(FlaskForm):
    weight = FloatField(_("Weight (in kg)"), validators=[DataRequired()])
    submit = SubmitField(_("Submit"))
