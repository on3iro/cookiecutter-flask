# -*- coding: utf-8 -*-
"""
Contains basic routes and helper functions
"""

from flask import render_template, Blueprint

from {{cookiecutter.app_name}}.extensions import login_manager
from {{cookiecutter.app_name}}.users.models import User


main_blueprint = Blueprint('main', __name__, url_prefix='',
                           static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


##########
# Routes #
##########
@main_blueprint.route('/')
def index():
    """Renders the index page."""
    return render_template('index.html')
