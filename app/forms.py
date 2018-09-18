from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, PasswordField, BooleanField, SubmitField,DateField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
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
    number = StringField('Number', validators=[DataRequired(), Length(min=1, max=139)])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=139)])
    value = IntegerField('Value', validators=[DataRequired()])
    timestamp  = DateField('Date Recieved', format='%d/%m/%y')
    client = StringField('Client', validators=[DataRequired(), Length(min=1, max=139)])
    submit = SubmitField('Create Project')
 
class TaskForm(FlaskForm):
    title = StringField('Task', validators=[DataRequired(), Length(min=1, max=139)])
    description = TextAreaField('About the Task', validators=[Length(min=1, max=139)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=1, max=49)])
    submit = SubmitField('Add Task')
 
class TaskCompleteForm(FlaskForm):
    duration = IntegerField('Task Time', validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Done')
    