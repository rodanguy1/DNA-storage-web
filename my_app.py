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
app.config['SECRET_KEY'] = key
choices = [['a', 'analysis 1'], ['b', 'analysis 2'], ['c', 'analysis 3'],
           ['d', 'analysis 4'], ['e', 'analysis 5']]


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/examples" ,methods=['GET', 'POST'])
def examples():
    print("DEBUG in exampples")
    debugPrint(os.getcwd())
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
    debugPrint("in upload")
    form = ToolForm()
    if form.validate_on_submit():
        debugPrint("if was good")
        form_files = [form.design.data, form.after_align.data, form.after_matching.data, form.reads.data]
        run_id = random.getrandbits(100)
        SaveFilesOnServer(form_files, run_id)
        tool_path = get_tool_path()
        email = form.email
        analyzes = form.analysis.data
        threading.Thread(target=RunDNATool, args=(tool_path, run_id, str.join(',', analyzes), email.data)).start()
        return redirect(url_for('after_run'))
    else:
        for err in form.errors:
            debugPrint(err)
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
        debugPrint('IN MAIN')
        app.run(debug=True)
    except Exception as e:
        print(e.message)
