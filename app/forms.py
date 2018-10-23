from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, PasswordField,
    BooleanField, SubmitField, DateField, TextAreaField)
from wtforms.validators import (
    DataRequired, ValidationError, Email, EqualTo, Length, NumberRange)
from .models import User
from wtforms.widgets import HTMLString
from wtforms.widgets.core import html_params


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ProjectForm(FlaskForm):
    number = StringField(
        'Number', validators=[DataRequired(), Length(min=1, max=139)])
    name = StringField(
        'Name', validators=[DataRequired(), Length(min=1, max=139)])
    value = IntegerField('Value', validators=[DataRequired()])
    timestamp = DateField('Date Recieved', format='%d/%m/%y')
    client = StringField(
        'Client', validators=[DataRequired(), Length(min=1, max=139)])
    submit = SubmitField('Create Project')


class TaskForm(FlaskForm):
    title = StringField(
        'Task', validators=[DataRequired(), Length(min=1, max=139)])
    genre = StringField(
        'Genre', validators=[DataRequired(), Length(min=1, max=49)])
    submit = SubmitField('Add Task')


class InlineButtonWidget(object):
    """
    Render a basic ``<button>`` field.
    """
    input_type = 'submit'
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('value', field.label.text)
        return HTMLString(
            '<button %s><i class="material-icons">done</i></button>' % 
            self.html_params(name=field.name, **kwargs))


class InlineSubmitField(BooleanField):
    """
    Represents an ``<button type="submit">``.  This allows checking if a given
    submit button has been pressed.
    """
    widget = InlineButtonWidget()


class TaskCompleteForm(FlaskForm):
    duration = IntegerField(
        'Task Time',
        validators=[DataRequired(), NumberRange(min=1, max=10000)])
    submit = InlineSubmitField('complete')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
