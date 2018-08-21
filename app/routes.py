from app import app
from flask import render_template, flash, redirect, url_for
from .forms import LoginForm
from flask_login import current_user, login_user
from .models import User

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Brian'}
    projects = [
        {
            'number': 134,
            'name': 'Temple Villa Road',
            'type':'Rear Extension',
            'value': 400
        },
        {
            'number': 185,
            'name':   'Electric Ave.',
            'type':   'Loft Conversion',
            'value':  350
        },
    ]
    return render_template('index.html', title='Home', user=user, projects=projects)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))    
    return render_template('login.html', title='Sign In', form=form)