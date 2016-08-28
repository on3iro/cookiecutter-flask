# -*- coding: utf-8 -*-
"""Functional tests using WebTest"""
from flask import url_for, render_template

from {{cookiecutter.app_name}}.users.forms import LoginForm
from {{cookiecutter.app_name}}.users.models import User


class TestMain:
    """Main functionality."""

    def test_root_resolves_to_main_view(self, testapp):
        assert url_for('main.index') == '/'

    def test_index_returns_200(self, testapp):
        """Test if index.html gets rendered"""
        # Goes to index route
        res = testapp.get('/')
        assert res.status_code == 200


class TestLoggingIn:
    """User related functionality."""

    def test_render_login_template(self, testapp):
        """Tests if the right template is rendered."""
        res = testapp.get(url_for('users.login'))
        form = LoginForm()
        assert res.status_code == 200
        assert res.text == render_template('users/login.html', form=form)

    def test_login_user(self, testapp, user):
        """Tests if a user is able to successfully login."""
        # Goes to /users/login page
        res = testapp.get(url_for('users.login'))

        # Fills out the login form
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'

        # Submits the form
        res = form.submit().follow()

        assert res.status_code == 200
        assert 'Logged in successfully' in res
        assert 'Logout' in res.text

    def test_user_sees_alert_on_logout(self, testapp, user):
        """Checks if user successfully logs out."""
        # Goes to /users/login page
        res = testapp.get(url_for('users.login'))

        # Fills out the login form
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'

        # Submits the form
        res = form.submit().follow()

        # Logs out
        res = testapp.get(url_for('users.logout')).follow()

        assert 'You are logged out' in res

    def test_login_form_fields_are_required(self, testapp, user):
        """Checks if form errors for invalid field data
        are flashed correctly."""
        # Goes to /users/login page
        res = testapp.get(url_for('users.login'))

        # Fills out the login form with invalid username and password
        form = res.forms['loginForm']
        form['username'] = ''
        form['password'] = ''

        # Submits the form
        res = form.submit()

        assert 'Username - This field is required.' in res
        assert 'Password - This field is required.' in res

    def test_invalid_password_or_username(self, testapp, user):
        """Checks if error flashes for wront password."""
        # Goes to /users/login page
        res = testapp.get(url_for('users.login'))

        # Fills out the login form with wront password
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'

        # Submits the form
        res = form.submit()

        assert 'Invalid user or password' in res


class TestRegistration:
    """Test class for registration tests."""

    def test_render_register_template(self, testapp):
        """Tests if the registration template is rendered"""
        # Goes to /users/register page
        res = testapp.get(url_for('users.register'))

        assert res.status_code == 200
        assert 'Please Register' in res.text

    def test_user_can_register(self, testapp, user):
        """Tests that users are able to register and that the data
        is committed to the database."""
        # Gets old number of users
        old_count = len(User.query.all())

        # Goes to /users/register page
        res = testapp.get(url_for('users.register'))

        # Gets register form
        form = res.forms['registerForm']

        # Fills form
        form['username'] = 'ttester'
        form['email'] = 'ttester@test.com'
        form['password'] = '123456'
        form['confirm'] = '123456'

        res = form.submit().follow()

        assert res.status_code == 200
        assert len(User.query.all()) == old_count + 1

    def test_cant_register_when_user_exists(self, testapp, user):
        """Test that a user whose email or username matches an
        existing user cannot register."""
        # Goes to /users/register page

        res = testapp.get(url_for('users.register'))

        # Gets register form
        form = res.forms['registerForm']

        # Fills form with same name and email as existing user
        form['username'] = 'testuser'
        form['email'] = user.email
        form['password'] = '123456'
        form['confirm'] = '123456'

        res = form.submit()

        assert 'That username and/or email is already in use.' in res

    def test_register_form_fields_are_required(self, testapp, user):
        """Checks if form errors for invalid field data
        are flashed correctly."""
        # Goes to /users/login page
        res = testapp.get(url_for('users.register'))

        # Fills out the login form with invalid username and password
        form = res.forms['registerForm']
        form['username'] = ''
        form['email'] = ''
        form['password'] = ''
        form['confirm'] = ''

        # Submits the form
        res = form.submit()

        assert 'Username - This field is required.' in res
        assert 'Password - This field is required.' in res
        assert 'Verify Password - This field is required.' in res
        assert 'Email - This field is required.' in res
