from flask_wtf import FlaskForm, widgets
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# def validate_multiple(form, field):
#     if len(field.data) == 0:
#         raise ValidationError('please choose your analysis')
#
#
# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()


class ToolForm(FlaskForm):
    design = FileField('Enter Your Design CSV File:',
                       validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only')])
    after_align = FileField('Enter Your After alignment CSV File:',
                            validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only')])
    analysis = SelectMultipleField('analysis'
                                   )


choices = ['analysis 1', 'analysis 2', 'analysis 3', 'analysis 4', 'analysis 5',
           'analysis 6', 'analysis 7', 'analysis 8']
