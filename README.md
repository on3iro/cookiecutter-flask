# Cookiecutter for flask

[![Build Status](https://travis-ci.org/on3iro/cookiecutter-flask.svg)](https://travis-ci.org/on3iro/cookiecutter-flask)

This is a simple cookiecutter for flask. It is still a work in progress, but should work fine already. I drew a lot of inspiration from [slorias cookiecutter](https://github.com/sloria/cookiecutter-flask).

Detailed instructions of how to use this cookiecutter will follow...

## Currently integrated:
* Password hashing via Flask-Bcrypt
* bpython shell
* Testing with pytest, WebTest and pytest-flask
* Test coverage via coverage and pytest-cov
* Flask-Admin
* Flask-DebugToolbar
* Login management with Flask-Login
* Database migrations via Flask-Migrate
* Flask-SQLAlchemy
* Formhandling with Flask-WTF
* psycopg2 for postgre connections
* simple login and user registration

## Not (yet) integrated
* Frontend-Framework
* Asset-Bundler
* Caching
* wsgi-server


# Installation and basic Usage
__Note: cookiecutter-flask is currently only tested under python 3.5!__

### 1. Install cookiecutter

    pip install cookiecutter

### 2. Clone cookiecutter-flask

    cookiecutter https://github.com/on3iro/cookiecutter-flask.git

### 3. Preparation
I advice you to take a few seconds and initialize a git repository inside
your newly created cookiecutter. Then go on and create a virtualenvironment
(e.g with pyvenv or virtualenvwrapper). For production use some settings need
to be made available to flask (e.g. the secret key). Check those lines which
are marked with a ```TODO```-command inside **settings.py**. The secret key for
example can be stored inside an environment variable.
To store your environment variable inside the virtualenvironment just add a
line like the following to **env/bin/activate**:
    
    <YOUR_APP_NAME>_SECRET='extremely_secret_key_you_wont_be_able_to_guess'

To quickly generate a secret key you can use open the interactive python shell,
and type the following commands:

```>> import os```
```>> os.urandom(24)```

Then copy the generated key.

### 4. Install Requirements
Activate your virtualenvironment with:
    
    source <name_of_your_venv>/bin/activate

Now simply install all python dependencies from requirements.txt:
    
    pip install -r requirement.txt

### 5. Project initialisation
To create your database, make an initial migration and create a default admin
user, follow these commands:

    ./manage.py db init
    ./manage.py db migrate
    ./manage.py db upgrade
    ./manage.py create_admin

### 6. Working with cookiecutter-flask

#### Running the server
    
    ./manage.py server

#### Testing the application

    ./manage.py test

#### Generating test coverage information

    py.test --cov=<app_name> --cov-report=html

(This will probably become a manage.py command as well in the future)

#### Migration the database

    ./manage.py migrate
    ./manage.py upgrade

(Note that it is advised to check migrations before upgrading!)

### Initial routes
For login/logout routes have a look a the respective views.py files.

__localhost:5000__: index view

__localhost:5000/users/__: member page (login required)

__localhost:5000/users/register__: user registration (a newly registered user
will be inactiv and has to be activated inside the admin panel!)

__localhost:5000/admin/__: admin index page (login required, user hast to be an
admin)

__localhost:5000/admin/user/__: admin panel for user model

__localhost:5000/admin/role/__: admin panel for role model
