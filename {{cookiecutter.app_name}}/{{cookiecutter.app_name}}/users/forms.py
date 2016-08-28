# -*- coding: utf-8 -*-
"""Forms for user registration and login"""
from flask_wtf import Form
from wtforms import PasswordField, StringField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length

from {{cookiecutter.app_name}}.database import db
from {{cookiecutter.app_name}}.users.models import User


####################
# Helper functions #
####################

def get_user(form):
    """Gets the user by the username of the form.data."""
    return (
        db.session.query(User)
        .filter_by(username=form.username.data).first()
    )


#####################
# Custom validators #
#####################

def validate_login(form, field):
    """Checks if a certain user exists, and if the forms hashed password
    matches the hash inside the database."""
    user = get_user(form)

    if user is None:
        raise validators.ValidationError('Invalid user or password')

    # compare plaintext pw with the hash from the db
    if not user.check_password(form.password.data):
        raise validators.ValidationError('Invalid user or password')


def is_admin(form, field):
    """Checks if a certain user is an admin and otherwise throws a
    validation error."""
    user = get_user(form)
    if not user.is_admin:
        raise validators.ValidationError('Invalid user or password')


#########
# Forms #
#########

class RegisterForm(Form):
    """Register form."""

    username = StringField('Username', validators=[DataRequired(),
                           Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email(),
                                             Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=6, max=50)])
    confirm = PasswordField('Verify Password',
                            validators=[DataRequired(),
                                        EqualTo('password',
                                        message='Passwords must match')])


class LoginForm(Form):
    """Basic login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     validate_login])


class AdminLoginForm(LoginForm):
    """Admin login form. Only users with the 'is_admin' flag pass the form
    validation."""
    password = PasswordField('Password', validators=[DataRequired(),
                                                     validate_login,
                                                     is_admin])
