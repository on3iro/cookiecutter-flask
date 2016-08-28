# -*- coding: utf-8 -*-
"""Tests app.py functionality"""
from {{cookiecutter.app_name}}.app import render_error, parse_401_to_404


class TestErrorhandlers:
    """Tests registered errorhandlers."""

    def test_default_500(self, app):
        with app.test_request_context():
            rendered_error = render_error('')
        assert 500 in rendered_error

    def test_fallback_to_404_on_401(self, app):
        error_code = parse_401_to_404(401)
        assert error_code == 404
