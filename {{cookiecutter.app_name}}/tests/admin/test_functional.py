# -*- coding: utf-8 -*-
"""Functional tests for flask_admin using Webtest"""
from flask import url_for
from pytest import raises


class TestAuth:

    def test_admin_index_redirects_to_admin_login(self, testapp):
        # Go to /admin/ page
        res = testapp.get(url_for('admin.index')).follow()
        assert 'Username' in res
        assert 'Password' in res

    def test_admins_can_login_to_admin_views(self, testapp, admin):
        """Tests if admin users get access to admin views."""
        # Go to /admin/ page
        res = testapp.get(url_for('admin.login_view'))

        # Get form
        form = res.form

        # Enter admin data
        form['username'] = admin.username
        form['password'] = 'admin'

        res = form.submit().follow()

        assert res.status_code == 200

    def test_non_admin_users_cannot_login(self, testapp, user):
        """Tests if normal users get redirected to a 404."""
        # Go to /admin/ page
        res = testapp.get(url_for('admin.login_view'))

        # Get form
        form = res.form

        # Enter user data
        form['username'] = user.username
        form['password'] = 'myprecious'

        res = form.submit()

        assert 'Invalid user or password' in res

    def test_unauthorized_user_get_404_on_access(self, testapp, user):
        """Tests if an unauthorized person gets a 404 when he attempts
        to access an adminview."""
        # Go to /admin/user
        res = testapp.get('/admin/user')
        with raises(Exception) as e_info:
            res.follow()
            assert '404' in e_info

    def test_admins_can_logout(self, testapp, admin):
        # Go to /admin/ page
        res = testapp.get(url_for('admin.login_view'))

        # Get form
        form = res.form

        # Enter admin data
        form['username'] = admin.username
        form['password'] = 'admin'

        res = form.submit().follow()

        # Logout
        res = testapp.get(url_for('admin.logout_view')).follow()
        print(res.text)

        assert 'Username' in res
        assert 'Password' in res
