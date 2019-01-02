from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, required
from wtforms.widgets import CheckboxInput, ListWidget

choices = [['a', 'analysis 1'], ['b', 'analysis 2'], ['c', 'analysis 3'],
           ['d', 'analysis 4'], ['e', 'analysis 5']]

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


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ToolForm(FlaskForm):
    design = FileField('Enter your Design CSV file:',
                       validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only')])
    after_align = FileField('Enter your After-Alignment CSV file:',
                            validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only')])
    after_matching = FileField('Enter your After-Matching CSV file:',
                            validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only')])
    reads = FileField('Enter your Reads file:',
                            validators=[FileRequired(), FileAllowed(['fastq'], 'fastq files only')])

    analysis = MultiCheckboxField(
        'Please Choose Your Analyzes: (at least one analysis)', coerce=str,
        choices=choices )
    email = StringField('Please Enter Your Email:', validators=[DataRequired(), Email()])
