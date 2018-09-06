from app import app, db
from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm, RegistrationForm, ProjectForm, TaskForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Project, Task
from werkzeug.urls import url_parse

# ------------------------------------------------------- HOME
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')
    

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
    return render_template('forms/login.html', title='Sign In', form=form)
  
    
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
    return render_template('forms/register.html', title='Register', form=form)



# ------------------------------------------------------- ALL PROJECTS
@app.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    jobs = Project.query.filter_by(user_id=user.id)
    return render_template('user.html', user=user, jobs=jobs)


    
# ------------------------------------------------------- NEW PROJECT
@app.route('/<username>/add_project', methods=['GET', 'POST'])
@login_required
def add_project(username):
    # user = User.query.filter_by(username=username).first_or_404()
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            number=form.number.data,
            name = form.name.data,
            value=form.value.data,
            client=form.client.data,
            user=current_user
            )
        db.session.add(project)
        db.session.commit()
        flash('Congratulations, you created a Project')
        return redirect(url_for('index'))
    return render_template('forms/add_project.html', form=form)


# ------------------------------------------------------- ALL PROJECTS
@app.route('/<username>/<projectno>')
@login_required
def view_project(username, projectno):
    # user = User.query.filter_by(username=username).first_or_404()
    # project = Project.query.filter_by(id=projectno)
    return render_template('project_page.html')
    


@app.route('/<username>/<projectno>/add_task', methods=['GET', 'POST'])
@login_required
def add_task(username, projectno):
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description = form.description.data,
            genre=form.genre.data,
            project_id=int(projectno)
            )
        db.session.add(task)
        db.session.commit()
        flash('Congratulations, you created a Task')
        return redirect(url_for('index'))
    return render_template('forms/add_task.html', form=form)