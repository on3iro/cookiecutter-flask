# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py"""
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


# Brypt
bcrypt = Bcrypt()

# CSRF protection
csrf_protect = CsrfProtect()

# Database/SQLAlchemy/Migrations
db = SQLAlchemy()
migrate = Migrate()

# Debug toolbar
debug_tb = DebugToolbarExtension()


###############################
# Login manager configuration #
###############################

login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "warning"
