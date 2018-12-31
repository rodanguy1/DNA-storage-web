import threading
from flask import render_template, url_for, flash, redirect
from flask_wtf.csrf import CSRFError
from werkzeug.utils import secure_filename
from utils.common import debug_print, run_dna_tool
from utils.config import *
from utils.forms import RegistrationForm, LoginForm, ToolForm

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


@app.route("/examples")
def examples():
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
        design_file = form.design.data
        file_name = secure_filename(design_file.filename)
        design_path = get_dir() + os.sep + 'outputs' + os.sep + file_name
        design_file.save(design_path)
        after_align_file = form.after_align.data
        file_name = secure_filename(after_align_file.filename)
        after_align_path = get_dir() + os.sep + 'outputs' + os.sep + file_name
        after_align_file.save(after_align_path)
        tool_path = get_tool_path()
        email = form.email
        analyzes = form.analysis.data
        threading.Thread(target=run_dna_tool,
                         args=(tool_path, after_align_path, design_path, str.join(',', analyzes), email.data)).start()
        return redirect(url_for('after_run'))
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
    app.run(debug=True)
