from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, PasswordField, BooleanField, SubmitField,DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
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
    number = StringField('Project Number', validators=[DataRequired(), Length(min=1, max=139)])
    name = StringField('Project Name', validators=[DataRequired(), Length(min=1, max=139)])
    value = IntegerField('Project Value', validators=[DataRequired()])
    timestamp  = DateField('Date Recieved', format='%m/%d/%y')
    submit = SubmitField('Create Project')
    