import random
import threading
from flask import render_template, url_for, flash, redirect, request
from flask_wtf.csrf import CSRFError

from utils.common import *
from utils.config import *
from utils.forms import RegistrationForm, LoginForm, ToolForm

# todo: create database API and implement it in register/login.html


db, app = get_app(__name__)
app.config['SECRET_KEY'] = key
choices = [['a', 'analysis 1'], ['b', 'analysis 2'], ['c', 'analysis 3'],
           ['d', 'analysis 4'], ['e', 'analysis 5']]



@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413


@app.route("/")
def home():
    debug_print("home page")
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
    debug_print("tool page")
    form = ToolForm(choices=choices)
    form.analysis.choices = choices
    return render_template('tool.html', form=form)


@app.route("/after_run")
def after_run():
    debug_print("after_run page")
    return render_template('after_run.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        debug_print("in upload")
        form = ToolForm()
        if form.validate_on_submit():
            debug_print("if was good")
            form_files = [form.design.data, form.after_align.data, form.after_matching.data, form.reads.data]
            run_id = random.getrandbits(100)
            save_files_on_server(form_files, run_id)
            dna_tool_path = get_tool_path()
            email1 = form.email
            analyzes = form.analysis.data
            threading.Thread(target=run_dna_tool,
                             args=(dna_tool_path, run_id, str.join(',', analyzes), email1.data)).start()
            return redirect(url_for('after_run'))
        else:
            debug_print("The Form didnt pass validation on submit")
            for err in form.errors:
                debug_print(err)
            debug_print(form.errors)
            return render_template('tool.html', title='DNA-STORAGE-TOOL', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    debug_print("register page")
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for ' + form.username.data, 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    debug_print("login page")
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
    try:
        debug_print('IN MAIN')
        app.run(debug=True)
    except Exception as e:
        print(e.message)
