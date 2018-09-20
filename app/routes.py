from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from .forms import LoginForm, RegistrationForm, ProjectForm, TaskForm, TaskCompleteForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Project, Task
from werkzeug.urls import url_parse
from sqlalchemy.orm import lazyload

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
        return redirect(url_for('user',  username=username))
    return render_template('forms/add_project.html', form=form)


# ------------------------------------------------------- SINGLE PROJECTS
@app.route('/<username>/<projectno>')
@login_required
def view_project(username, projectno):
    form = TaskCompleteForm()
    tasks = Task.query.filter_by(project_id=projectno)
    job = Project.query.filter_by(id=projectno).first_or_404()
    print(len(tasks[0:]))
    return render_template('project_page.html', tasks=tasks, job=job, form=form)
    

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
        # If all task are complete, when new task added mark project as not complete
        are_all_tasks_complete = len({task.completed for task in Task.query.filter_by(project_id=int(projectno))})
        if are_all_tasks_complete == 1:
            project = Project.query.filter_by(id=int(projectno)).first_or_404()
            project.completed = False
        db.session.add(task)
        db.session.commit()
        flash('Congratulations, you created a Task')
        return redirect(url_for('view_project',  username=username, projectno=projectno))
        
    user = User.query.filter(User.username == username)[0]
    list_of_genres = [project.tasks.all() for project in Project.query.join(Task, (Task.project_id==Project.id)).all() if project.user_id==user.id]
    genres = sorted({item.genre for sublist in list_of_genres for item in sublist}) 
    return render_template('forms/add_task.html', form=form, genres=genres)
    

@app.route('/<username>/<projectno>/delete_task/<task_id>')
def delete_task(task_id, username, projectno):
    task = Task.query.filter_by(id=int(task_id)).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_project',  username=username, projectno=projectno))


@app.route('/<username>/<projectno>/task_complete/<task_id>', methods=['GET', 'POST'])
def complete_task(task_id, username, projectno):
    form = TaskCompleteForm()
    if form.validate_on_submit():
        
        # Complete Task
        task = Task.query.filter_by(id=int(task_id)).first_or_404()
        task.duration = form.duration.data
        task.completed = True
        db.session.commit()
        
        # Complete project if all task are complete
        are_all_tasks_complete = len({task.completed for task in Task.query.filter_by(project_id=int(projectno))})
        if are_all_tasks_complete == 1:
            project = Project.query.filter_by(id=int(projectno)).first_or_404()
            project.completed = True
            db.session.commit()
    return redirect(url_for('view_project',  username=username, projectno=projectno))

@app.route('/<username>/<projectno>/task_not_complete/<task_id>')
def complete_not_task(task_id, username, projectno):
    are_all_tasks_complete = len({task.completed for task in Task.query.filter_by(project_id=int(projectno))})
    if are_all_tasks_complete == 1:
        project = Project.query.filter_by(id=int(projectno)).first_or_404()
        project.completed = False
    task = Task.query.filter_by(id=int(task_id)).first_or_404()
    task.completed = False
    db.session.commit()
    return redirect(url_for('view_project',  username=username, projectno=projectno))


@app.route('/<username>/data')
@login_required
def user_data(username):
    user_projects=Project.query.join(User, (User.id==Project.user_id)).filter(User.username == username)
    # project_tasks = Project.query.options(lazyload('tasks')).filter_by(User.username == username)[0].tasks.all()
    
    data = [
        {
            'user':job.user.username, 
            'project_title':job.name,
            'project_id':job.id,
            'project_value':job.value,
            'project_client':job.client,
            'project_completed':sum([job.completed]),
            'project_recieved':job.timestamp,
            'project_tasks_all':len(job.tasks.all()),
            'project_tasks_completed':sum([task.completed for task in job.tasks.all()])
        } 
        for job in user_projects] 
    
    return jsonify(data)
    
