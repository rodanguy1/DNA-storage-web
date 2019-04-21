import itertools
import json
import os
import smtplib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

# ############# WORKING DIR #####################################
input_files_dir = 'input_files_dir'
tool_name = 'main.py'
sep = os.sep
# basedir = 'C:' + sep + 'Users' + sep + 'grodan' + sep + 'PycharmProjects' + sep + 'DNA-storage-web'
basedir = os.getcwd()
tool_path = basedir + sep + 'utils' + sep + tool_name
tool_sub_path = sep+'eitans_files'+sep+'Library-Analyzer-master'+sep
# ############# SET EMAIL #####################################

config = []

if os.environ.get('mode') == 'prod':
    basedir = '/home/omersabary/DNA-storage-web'
    with open('/etc/config.json') as config_file:
        config = json.load(config_file)
    email = config.get('email')
    password = config.get('email_password')
    key = config.get('secret_key')
else:
    email = os.environ.get('email')
    password = os.environ.get('email_password')
    key = os.environ.get('secret_key')
mail = None
try:
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(email, password)
    mail = gmail
except:
    print("Couldn't setup email!!")


# ############# APP CONFIG #####################################


def get_app(name):
    csrf = CsrfProtect()
    app = Flask(name)
    # todo: make in an env var
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    app.config['SECRET_KEY'] = key
    app.config['WTF_CSRF_SECRET_KEY'] = key
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = email
    app.config['MAIL_PASSWORD'] = password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024
    db = SQLAlchemy(app)
    csrf.init_app(app)
    return db, app


# ############## RUN ID ##############################
_counter = itertools.count()


def get_id():
    return next(_counter)


def get_tool_path():
    tool_path = get_dir() + tool_sub_path + tool_name
    return tool_path


def get_dir():
    return basedir


def get_mail():
    return mail
