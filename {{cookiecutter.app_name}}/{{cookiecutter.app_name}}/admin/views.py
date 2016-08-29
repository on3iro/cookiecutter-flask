# -*- coding: utf-8 -*-
"""Admin views."""
import flask_admin as admin
import flask_login as login

from flask import redirect, url_for, request, abort
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from {{cookiecutter.app_name}}.users.forms import AdminLoginForm, get_user


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        """Override builtin handle_view in order to redirect users when a
        view is not accessible."""
        if not self.is_accessible():
            abort(404)


# Create customized view for user models
class UserView(MyModelView):
    """Flask user model view."""
    create_modal = True
    edit_modal = True

    # Remove password field from form
    form_excluded_columns = ('password')

    # Add dummy password field
    form_extra_fields = {
        'password_dummy': PasswordField('Password')
    }

    # Set the form fields to use
    form_columns = (
        'username',
        'email',
        'first_name',
        'last_name',
        'password_dummy',
        'created_at',
        'active',
        'is_admin'
    )

    def on_model_change(self, form, User, is_created):
        # Set password if password_dummy is set
        if (form.password_dummy.data != ''
                and form.password_dummy.data is not None):
            User.set_password(form.password_dummy.data)

# Create customized index view class taht handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    """Flask Admin view. Only Users with the 'is_admin' flag
    have access."""

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = AdminLoginForm(request.form)

        if helpers.validate_form_on_submit(form):
            user = get_user(form)
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.login_view'))
