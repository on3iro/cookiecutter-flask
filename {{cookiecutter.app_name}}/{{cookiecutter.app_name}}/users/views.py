# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, flash, url_for, redirect, \
    request
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, login_user, logout_user

from {{cookiecutter.app_name}}.database import db
from {{cookiecutter.app_name}}.utils import flash_errors
from {{cookiecutter.app_name}}.users.forms import RegisterForm, LoginForm, get_user
from {{cookiecutter.app_name}}.users.models import User

users_blueprint = Blueprint('users', __name__, url_prefix='/users',
                            static_folder='../static')


##########
# Routes #
##########

@users_blueprint.route('/')
@login_required
def members():
    """Member page."""
    return render_template('users/members.html')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login form and logs in the user,
    if valid credentials are provided."""
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Login and validate the user
            user = get_user(form)
            login_user(user)

            flash('Logged in successfully.')

            return redirect(url_for('users.members'))
        else:
            flash_errors(form)

    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    """Logs out the user"""
    logout_user()
    flash('You are logged out.')
    return redirect(url_for('users.login'))


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Renders the registration form and registers user on submit.
    Note that by default users are inactive and need to be activated inside
    flask_admin."""
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Registers user
            new_user = User(
                username=form.username.data,
                email=form.email.data
            )

            # Hash password
            new_user.set_password(form.password.data)

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful. Please sign in.')
                return redirect(url_for('users.login'))
            except IntegrityError:
                flash('That username and/or email is already in use.', 'error')
                return render_template('users/register.html',
                                       form=form)
        else:
            flash_errors(form)

    return render_template('users/register.html', form=form)
