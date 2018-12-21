from flask_wtf import FlaskForm, widgets
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import CheckboxInput, ListWidget

choices = [['analysis 1', 'analysis 1'], ['analysis 2', 'analysis 2'], ['analysis 3', 'analysis 3'],
           ['analysis 4', 'analysis 4'], ['analysis 5', 'analysis 5']]


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


def validate_multiple(form, field):
    if len(field.data) == 0:
        raise ValidationError('please choose your analysis')
#
#
# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ToolForm(FlaskForm):
    design = FileField('Enter Your Design CSV File:',
                       validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only')])
    after_align = FileField('Enter Your After alignment CSV File:',
                            validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only')])
    analysis = MultiCheckboxField(
        'Please Choose Your Analyzes: (at least one analysis)',
        choices=choices, validators=[validate_multiple]
    )
