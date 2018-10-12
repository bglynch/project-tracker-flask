from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify, abort
from .forms import LoginForm, RegistrationForm, ProjectForm, TaskForm, TaskCompleteForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Project, Task
from werkzeug.urls import url_parse
from sqlalchemy.orm import lazyload
from app.email import send_password_reset_email

# ------------------------------------------------------- HOME
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('dashboard.html', title='Home')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=(form.email.data).lower()).first()
        
        # Error logging in
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
        user = User(
            username=(form.username.data).lower(), 
            email=form.email.data
            )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('forms/register.html', title='Register', form=form)


# ------------------------------------------------------- ALL PROJECTS
@app.route('/projects')
@login_required
def view_projects():
    jobs = Project.query.filter_by(user_id=current_user.id)
    return render_template('projects.html', jobs=jobs)


# ------------------------------------------------------- NEW PROJECT
@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            number=form.number.data,
            name = form.name.data.lower(),
            value=form.value.data,
            client=form.client.data,
            user=current_user
            )
        db.session.add(project)
        db.session.commit()
        flash('Congratulations, you created a Project')
        return redirect(url_for('view_projects'))
    return render_template('forms/add_project.html', title="Create Project",  form=form)


# ------------------------------------------------------- SINGLE PROJECTS
@app.route('/project/<projectno>')
@login_required
def view_project_tasks(projectno):
    form = TaskCompleteForm()
    tasks = Task.query.filter_by(project_id=projectno)
    job = Project.query.filter_by(id=projectno).first_or_404()
    if job.user_id == current_user.id:
        return render_template('projects_tasks.html', tasks=tasks, job=job, form=form)
    else:
        return redirect(url_for('view_projects'))

    
@app.route('/project/<int:projectno>/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project(projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()
    if job.user_id != current_user.id:
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        job.number=form.number.data
        job.name = form.name.data.lower()
        job.value=form.value.data
        job.client=form.client.data    
        db.session.commit()
        flash('Your project has been updated!')
        return redirect(url_for('view_project_tasks', projectno=projectno))
    elif request.method == 'GET':
        form.number.data = job.number
        form.name.data = job.name
        form.value.data = job.value
        form.client.data = job.client
    return render_template('forms/add_project.html', title="Edit Project", form=form)

    
@app.route('/project/<int:projectno>/delete_project', methods=['GET', 'POST'])  
@login_required
def delete_project(projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()
    if job.user_id != current_user.id:
        abort(403)
    db.session.delete(job)
    db.session.commit()
    flash('Project successfully deleted')
    return redirect(url_for('view_projects'))


@app.route('/project/<projectno>/add_task', methods=['GET', 'POST'])
@login_required
def add_task(projectno):
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
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
        return redirect(url_for('view_project_tasks', projectno=projectno))
    
    elif request.method == "GET":    
        job = Project.query.filter_by(id=projectno).first_or_404()
        user = User.query.filter(User.id == current_user.id)[0]
        list_of_genres = [project.tasks.all() for project in Project.query.join(Task, (Task.project_id==Project.id)).all() if project.user_id==user.id]
        genres = sorted({item.genre for sublist in list_of_genres for item in sublist}) 

        if job.user_id == current_user.id:
            return render_template('forms/add_task.html', title='Create Task', form=form, genres=genres)
        else:
            flash('Not able to add task to projects that are not yours')
            return redirect(url_for('view_projects'))
    

@app.route('/project/<projectno>/delete_task/<task_id>')
def delete_task(task_id, projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()

    if job.user_id == current_user.id:
        task = Task.query.filter_by(id=int(task_id)).first_or_404()
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('view_project_tasks', projectno=projectno))
    else:
        flash('Not able to delete a task that is not yours')
        return redirect(url_for('view_projects'))


@app.route('/project/<projectno>/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id, projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()
    task = Task.query.get_or_404(task_id)
    list_of_genres = [project.tasks.all() for project in Project.query.join(Task, (Task.project_id==Project.id)).all() if project.user_id==current_user.id]
    genres = sorted({item.genre for sublist in list_of_genres for item in sublist}) 
    if job.user_id != current_user.id:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.genre = form.genre.data
        db.session.commit()
        flash('Your task has been updated!')
        return redirect(url_for('view_project_tasks', projectno=projectno))
    elif request.method == 'GET':
        form.title.data = task.title
        form.genre.data = task.genre
    return render_template('forms/add_task.html', title='Edit Task', form=form, genres=genres)

        
@app.route('/project/<projectno>/task_complete/<task_id>', methods=['GET', 'POST'])
def complete_task(task_id, projectno):
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
        
        return redirect(url_for('view_project_tasks', projectno=projectno))
    
    elif request.method == "GET":    
        job = Project.query.filter_by(id=projectno).first_or_404()
        if job.user_id == current_user.id:
            return redirect(url_for('view_project_tasks', projectno=projectno))
        else:
            flash('Not able to add task to modify tasks that are not yours')
            return redirect(url_for('view_projects'))


@app.route('/<projectno>/task_not_complete/<task_id>')
def task_not_complete(task_id, projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()
    if job.user_id == current_user.id:
        are_all_tasks_complete = len({task.completed for task in Task.query.filter_by(project_id=int(projectno))})
        if are_all_tasks_complete == 1:
            project = Project.query.filter_by(id=int(projectno)).first_or_404()
            project.completed = False
        task = Task.query.filter_by(id=int(task_id)).first_or_404()
        task.completed = False
        db.session.commit()
        return redirect(url_for('view_project_tasks', projectno=projectno))
    else:
        flash('Not able to add task to modify tasks that are not yours')
        return redirect(url_for('view_projects'))


@app.route('/data')
@login_required
def user_data():
    user_projects=Project.query.join(User, (User.id==Project.user_id)).filter(User.id == current_user.id)
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
 
    
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('forms/reset_password_request.html',
                           title='Reset Password', form=form)

                           
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('forms/reset_password.html', form=form)