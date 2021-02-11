"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import (DateTimeField, FloatField, PasswordField, SelectField,
                     StringField, SubmitField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

from .models import Tea


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class TeaAddForm(FlaskForm):
    """Tea creation form"""
    name = StringField(
        'Tea Name',
        validators=[DataRequired()]
    )
    price_per_gram = FloatField(
        'Price Per Gram'
    )
    submit = SubmitField('Create')


class TeaLogForm(FlaskForm):
    tea_choices = [
        (tea.id, tea.name) for tea in Tea.query.all()
    ]
    tea = SelectField(
        'Tea',
        validators=[DataRequired()], choices=tea_choices
    )
    date = DateTimeField(
        'Date',
        validators=[DataRequired()]
    )
    submit = SubmitField('Log')
