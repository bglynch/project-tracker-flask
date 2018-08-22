from app import app, db
from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm, RegistrationForm, ProjectForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
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
    return render_template('index.html', title='Home', projects=projects)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)        
    return render_template('login.html', title='Sign In', form=form)
  
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))    


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    projects = [
        {'user': user, 'number': '2018-282', 'name':'Electric Ave.', 'type':'Loft Conversion', 'value':350, 'completed':False},
        {'user': user, 'number': '2018-198', 'name':'Bond Road', 'type':'Rear Extension', 'value':400, 'completed':False},
        {'user': user, 'number': '2018-100', 'name':'Kettle Drive', 'type':'Survey', 'value':200, 'completed':False}
    ]
    return render_template('user.html', user=user, projects=projects)
    
@app.route('/user/<username>/add_project')
@login_required
def add_project(username):
    # user = User.query.filter_by(username=username).first_or_404()
    form = ProjectForm()
    return render_template('add_project.html', form=form)
    

