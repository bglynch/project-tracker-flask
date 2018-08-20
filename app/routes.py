from app import app
from flask import render_template, flash, redirect, url_for
from .forms import LoginForm

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
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))    
    return render_template('login.html', title='Sign In', form=form)