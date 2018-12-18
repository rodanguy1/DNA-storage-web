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
sep = os.sep
# basedir = 'C:' + sep + 'Users' + sep + 'grodan' + sep + 'PycharmProjects' + sep + 'DNA-storage-web'
basedir = os.getcwd()

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
    app = Flask(name)
    # todo: make in an env var
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    app.config['SECRET_KEY'] = os.environ.get('secret_key')  # '34533a9999c895e8da8a84fc029b88f8'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = email
    app.config['MAIL_PASSWORD'] = password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    db = SQLAlchemy(app)
    return db, app


def get_dir():
    return basedir

def DebugPrint(message):
    cur_time = datetime.datetime.now().time()
    print("\n*****DEBUG: "+str(cur_time)+" - " +str(message)+" ****************\n")


def RunApp(tool_path,alignment_path, design_path):
    cmd = sys.executable + ' ' + tool_path + ' ' + alignment_path + ' ' + design_path
    DebugPrint('b4 process')
    process_output = subprocess.check_output(cmd)
    DebugPrint('after process. output is :')
    DebugPrint(process_output)
    if os.path.exists(process_output):
        DebugPrint('file is existing')
    else:
        DebugPrint('file is none')


def send_results(email, run_id):
    msg = MIMEMultipart()
    msg['Subject'] = 'DNA-STORAGE-TOOL results'
    msg['To'] = ','.join([email])
    msg['From'] = os.environ.get('email')
    file = os.getcwd() + os.sep + 'utils' + os.sep + 'results.pdf'
    msg.attach(MIMEText(' your DNA-STORAGE-TOOL results of run  number: '+run_id+' are now available to Download'))
    with open(file, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(file)
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)
    try:
        mail.send_message(msg)
    except:
        print("COULDN'T SEND EMAIL")


# ############## RUN ID ##############################
_counter = itertools.count()


def get_id():
    return next(_counter)
