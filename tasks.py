#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Invoke tasks for automated builds."""
import os
import json
import shutil

from invoke import task, run

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

# Load cookiecutter.json
with open(os.path.join(CURRENT_DIR, 'cookiecutter.json'), 'r') as settings:
    COOKIECUTTER_SETTINGS = json.load(settings)

# Get default value of app_name from cookiecutter.json
COOKIE = os.path.join(CURRENT_DIR, COOKIECUTTER_SETTINGS['app_name'])
REQUIREMENTS = os.path.join(COOKIE, 'requirements', 'dev.txt')


@task
def build():
    """Build app from cookiecutter"""
    print('Building app...')
    run('cookiecutter {0} --no-input'.format(CURRENT_DIR))


@task
def clean():
    """Clean up generated cookiecutter app."""
    print('Removing {0}'.format(COOKIE))
    if os.path.exists(COOKIE):
        shutil.rmtree(COOKIE)
        print('Removed {0}'.format(COOKIE))
    else:
        print('App directory does not exist. Skipping clean up.')


def _run_manage_command(command):
    print('Running command "{0}"'.format(command))
    run('python {0} {1}'
        .format(os.path.join(COOKIE, 'manage.py'), command), echo=True)


@task(pre=[build], post=[clean])
def test():
    """Run tests."""
    print('Initializing tests...')
    run('pip install -r {0} --ignore-installed'
        .format(REQUIREMENTS), echo=True)
    print('Changing into app directory.')
    os.chdir(COOKIE)
    print('Running tests...')
    _run_manage_command('test')
