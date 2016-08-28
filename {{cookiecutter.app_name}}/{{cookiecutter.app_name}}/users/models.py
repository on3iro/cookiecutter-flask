# -*- coding: utf-8 -*-
"""User models."""
import datetime

from flask_login import UserMixin, AnonymousUserMixin

from {{cookiecutter.app_name}}.database import Column, Model, SurrogatePK, db, \
    reference_col, relationship
from {{cookiecutter.app_name}}.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name="", **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instsance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False,
                        default=datetime.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username="", email="", password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def __str__(self):
        """String representation of the user. Shows the users email address."""
        return self.email

    def set_password(self, password):
        """Set password"""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements"""
        return self.id

    @property
    def full_name(self):
        """Full user name."""
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def is_active(self):
        """Active or non active user (required by flask-login)"""
        return self.active

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
