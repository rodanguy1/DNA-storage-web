from flask import request, render_template, url_for, flash, redirect
# from utils import *
from utils.config import *
# get_app, send_results, get_id
from utils.forms import RegistrationForm, LoginForm
import subprocess
import sys
import os
import threading
# todo: shape the "after_run.html" template
# todo: create database API and implement it in register/login.html


db, app = get_app(__name__)
app.config['SECRET_KEY'] = '34533a9999c895e8da8a84fc029b88f8'


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



@app.route("/after_run")
def after_run():
    return render_template('after_run.html')





@app.route("/upload", methods=['GET', 'POST'])
def upload():
    input_valid = True
    try :
        design_file = request.files['design']
    except Exception as e:
        input_valid = False
        flash('You are missing the Design File.',"error")
    try:
        alignment_file = request.files['after_alignment']
    except:
        input_valid = False
        flash('You are missing the Alignment File.',"error")
    try:
        # todo: checl files format
        analysis = request.form.getlist('analysis')
    except:
        flash("You are didn't choose any analyzers.","error")
    analyser_given = False
    if len(analysis) > 0 :
        DebugPrint('the len is '+str(len(analysis)))
    for analysis_name in analysis:
        DebugPrint(analysis_name)
        if analysis_name == 'on':
            analyser_given = True
    DebugPrint('end of for')
    if analyser_given is False:
        flash("You are didn't choose any analyzers.","error")
        input_valid = False

    if input_valid is True:
        # TODO - change send_results()
        # send_results('rodanguy@gmail.com', 1)
        # TODO - check input is my responsibility?
        DebugPrint('legal params')
        design_path = ".\\" + design_file.filename
        design_file.save(design_path)
        alignment_path = ".\\" + alignment_file.filename
        alignment_file.save(alignment_path)
        tool_path = 'C:\Users\eitanfg\PycharmProjects\web\DNA-storage-web-new\DNA-storage-web\utils\mock_tool.py'
        if os.path.exists(tool_path):
            os.chmod(tool_path,777)
            DebugPrint(os.access(tool_path, os.X_OK))

        thread_for_app = threading.Thread(target=RunApp,args=(tool_path,alignment_path,design_path))
        thread_for_app.start()
        return redirect(url_for('after_run'))
    else:
        DebugPrint('bad params')
        return render_template('tool.html')





@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}', 'success')
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
