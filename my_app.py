import os

from flask import Flask, request, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime
app = Flask(__name__)
sep=os.sep

basedir = 'C:'+ sep +'Users'+ sep +'grodan'+ sep +'PycharmProjects'+ sep +'DNA-storage-web'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
# todo: make in an env var
app.config['SECRET_KEY'] = '34533a9999c895e8da8a84fc029b88f8'

db = SQLAlchemy(app)




results = [
    {
        'build_number': '4',
        'time_stamp': time.strftime("%H:%M:%S"),
        'result': 'Success'
    },
    {
        'build_number': '3',
        'time_stamp': time.strftime("%H:%M:%S"),
        'result': 'Success'
    },
    {
        'build_number': '2',
        'time_stamp': time.strftime("%H:%M:%S"),
        'result': 'Success'
    },
    {
        'build_number': '1',
        'time_stamp': time.strftime("%H:%M:%S"),
        'result': 'Success'
    },
]


@app.route("/")
def home():
    return render_template('home.html', results=results)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/examples")
def examples():
    return render_template('examples.html')


@app.route("/tool")
def tool():
    return render_template('tool.html')


@app.route("/upload")
def upload():
    file = request.files['input_file']

    return file.filename


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
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


if __name__ == '__main__':
    app.run(debug=True)
