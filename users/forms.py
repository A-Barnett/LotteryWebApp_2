import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo


def character_check(form, field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed.")


def validate_data(self, data_field):
    p = re.compile(r'[a-z]*[A-Z]*\d*\W')
    if not p.match(data_field.data):
        raise ValidationError("Password must contain at least one digit and one uppercase character")


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    firstname = StringField(validators=[DataRequired(), character_check])
    lastname = StringField(validators=[DataRequired(), character_check])
    phone = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12), validate_data])
    confirm_password = PasswordField(
        validators=[DataRequired(), EqualTo('password', message='Password fields must be equal')])
    submit = SubmitField()
