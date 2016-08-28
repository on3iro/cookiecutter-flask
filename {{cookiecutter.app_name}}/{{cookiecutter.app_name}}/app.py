# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template
from flask_admin import Admin

from {{cookiecutter.app_name}}.settings import ProdConfig
from {{cookiecutter.app_name}}.extensions import bcrypt, csrf_protect, db, migrate, \
    login_manager, debug_tb
from {{cookiecutter.app_name}}.main.views import main_blueprint
from {{cookiecutter.app_name}}.admin.views import MyModelView, MyAdminIndexView, UserView
from {{cookiecutter.app_name}}.users.views import users_blueprint
from {{cookiecutter.app_name}}.users.models import User, Role


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories.

    :param config_object: The configuration object to use.
    """

    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    init_admin(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    migrate.init_app(app, db)
    debug_tb.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(users_blueprint)
    app.register_blueprint(main_blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    for errcode in [401, 404, 500]:
        app.register_error_handler(errcode, render_error)

    return None


def init_admin(app):
    """Adds ModelViews to flask-admin."""
    admin = Admin(
        app,
        name="{{cookiecutter.app_name}}-Admin",
        index_view=MyAdminIndexView(),
        base_template='my_master.html',
        endpoint="admin"
    )
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(UserView(User, db.session))

    return None


####################
# Helper functions #
####################

def render_error(error):
    """Render error template"""
    # If a HTTPException, pull the `code` attribute; default to 500
    error_code = getattr(error, 'code', 500)

    error_code = parse_401_to_404(error_code)

    return render_template('{0}.html'.format(error_code)), error_code


def parse_401_to_404(error_code):
    """Parses a 401 error code to a 404."""

    # The user does not need to know that he is not
    # allowed to access a certain
    # resource. For security reasons the user should see the standard
    # 404 instead of an unauthorized error
    if error_code == 401:
        error_code = 404

    return error_code
