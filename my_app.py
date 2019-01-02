import threading
from flask import render_template, url_for, flash, redirect
from flask_wtf.csrf import CSRFError
from werkzeug.utils import secure_filename
from utils.common import *
from utils.config import *
from utils.forms import RegistrationForm, LoginForm, ToolForm
import random

# todo: create database API and implement it in register/login.html


db, app = get_app(__name__)
# app.config['SECRET_KEY'] = '34533a9999c895e8da8a84fc029b88f8'
choices = [['1', 'analysis 1'], ['2', 'analysis 2'], ['3', 'analysis 3'],
           ['4', 'analysis 4'], ['5', 'analysis 5']]


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/examples")
def examples():
    print("DEBUG in exampples")
    return render_template('examples.html')


@app.route("/tool")
def tool():
    form = ToolForm(choices=choices)
    form.analysis.choices = choices
    return render_template('tool.html', form=form)


@app.route("/after_run")
def after_run():
    return render_template('after_run.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    form = ToolForm()
    if form.validate_on_submit():
        form_files= [form.design.data,form.after_align.data,form.after_matching.data,form.reads.data]
        run_id = random.getrandbits(100)
        SaveFilesOnServer(form_files,run_id)
        tool_path = get_tool_path()
        email = form.email
        analyzes = form.analysis
        threading.Thread(target=RunDNATool, args=(tool_path,run_id, analyzes, email)).start()
        return redirect(url_for('after_run',email))
    else:
        debug_print(form.errors)
        return render_template('tool.html', title='DNA-STORAGE-TOOL', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for ' + form.username.data, 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'rodanguy@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    print(e.description)
    return redirect(url_for('tool'))


if __name__ == '__main__':
    # app.run(host='132.69.8.7', port=80 , debug=True)
     try:
         print "hello"
         app.run(debug=True)
     except Exception as e:
         print(e.message)


