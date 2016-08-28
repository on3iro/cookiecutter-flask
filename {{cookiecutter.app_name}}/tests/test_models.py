# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime

import pytest
from flask_login import AnonymousUserMixin

from {{cookiecutter.app_name}}.users.models import Role, User
from {{cookiecutter.app_name}}.main.views import load_user

from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User('foo', 'foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, datetime.datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self):
        """Test check password."""
        user = User.create(username='foo', email='foo@bar.com',
                           password='foobarbaz123')
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('lajfd') is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name='Foo', last_name='Bar')
        assert user.full_name == 'Foo Bar'

    def test_roles(self):
        """Add a role to a user."""
        role = Role(name='admin')
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles

    def test_string_representation(self):
        """Test string representation."""
        user = UserFactory(email="test@test.de")
        user.save()
        assert str(user) == 'test@test.de'

    def test_is_active(self):
        """Tests is_active method."""
        user = UserFactory(active=True)
        user.save()
        assert user.is_active

    def test_is_anonymous(self):
        """Test is_anonymous method."""
        user = UserFactory()
        user.save()
        assert user.is_anonymous is False

    def test_is_authenticated_is_true(self):
        """Test is_authenticated method."""
        user = UserFactory()
        user.save()
        assert user.is_authenticated is True

    def test_anon_user_is_authenticated_is_false(self):
        """Tests if user is instance of AnonymousUserMixin."""

        class AnonUser(User, AnonymousUserMixin):
            """Anonymous user."""

        anon_user = AnonUser(email="anon@anon.com", username="anon")
        anon_user.save()
        assert anon_user.is_authenticated is False


@pytest.mark.usefixtures('db')
class TestRole:
    """Role tests."""

    def test_role_representation(self):
        role = Role(name='user')
        role.save()
        assert str(role) == '<Role(user)>'


@pytest.mark.usefixtures('db')
def test_load_user():
    """Test load_user function."""
    user = User(email="ttester@test.com", username="ttester")
    user.save()
    assert user == load_user(user.get_id())
