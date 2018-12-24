import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import itertools
import datetime
import subprocess
import sys

# ############# WORKING DIR #####################################
from flask_wtf import CsrfProtect

sep = os.sep
# basedir = 'C:' + sep + 'Users' + sep + 'grodan' + sep + 'PycharmProjects' + sep + 'DNA-storage-web'
basedir = os.getcwd()
tool_name = 'mock_tool.py'
tool_path = basedir + sep + 'utils' + sep + tool_name
# ############# SET EMAIL #####################################
email = os.environ.get('email')
password = os.environ.get('email_password')
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
    app.config['SECRET_KEY'] = os.environ.get('secret_key')  # '34533a9999c895e8da8a84fc029b88f8'
    app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('secret_key')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = email
    app.config['MAIL_PASSWORD'] = password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    db = SQLAlchemy(app)
    csrf.init_app(app)
    return db, app


# ############## RUN ID ##############################
_counter = itertools.count()


def get_id():
    return next(_counter)


def get_tool_path():
    return tool_path


def get_dir():
    return basedir


def get_mail():
    return mail
