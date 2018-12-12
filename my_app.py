from flask import request, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from utils.config import get_app, send_results


#todo: get analizers input to mock function
#todo: shape the "after_run.html" template
#todo: create database API and implement it in register/login.html


db, app = get_app(__name__)


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
    return render_template('tool.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    file1 = request.files['design']
    file2 = request.files['after_alignment']
    # todo: checl files format
    send_results('rodanguy@gmail.com')
    return render_template('after_run.html')


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
