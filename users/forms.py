import re

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo


def character_check(form, field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed.")


def validate_data(self, data_field):
    p = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)')
    if not p.match(data_field.data):
        raise ValidationError("Password must contain at least one digit and one uppercase character")


def validate_phone(self, data_field):
    p = re.compile(r'\d{4}.*[-].*\d{3}.*[-].*\d{4}')
    if not p.match(data_field.data):
        raise ValidationError("Phone should be in format XXXX-XXX-XXXX")


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    firstname = StringField(validators=[DataRequired(), character_check])
    lastname = StringField(validators=[DataRequired(), character_check])
    phone = StringField(validators=[DataRequired(), validate_phone])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12), validate_data])
    confirm_password = PasswordField(
        validators=[DataRequired(), EqualTo('password', message='Password fields must be equal')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()
    #recaptcha = RecaptchaField()
    pin = StringField(validators=[DataRequired()])
