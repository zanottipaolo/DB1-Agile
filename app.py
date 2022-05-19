from cProfile import label
from datetime import date
import datetime
from time import strptime
from webbrowser import get
from flask import Flask, flash, redirect, render_template, request, url_for
import flask_login
from sqlalchemy import desc
from sqlalchemy import desc, func, true
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from sqlalchemy.orm import aliased

# Database
from backend.database import db_session

# Models
from backend.models import Sprint, Task, SubTask, Epic, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ciao'

# Log in manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Get the user from DB
        user = User.query.filter_by(email=email).first()

        # If not exists or pw not match
        if not user or not check_password_hash(user.password, password):
            flash('Check your login details and try again.', 'error')
            return redirect('/')

        login_user(user)
        return redirect(url_for('sprint'))
    else:
        return render_template('login.html', isNotLogin=False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')
        manager = request.form.get('manager', type=bool)

        # check if a user already exists
        user = User.query.filter_by(email=email).first()

        if user:  # if user is found --> redirect to Sign Up
            flash('Email already exists')
            return redirect(url_for('signup'))

        new_user = User(name=name, surname=surname, email=email, password=generate_password_hash(
            password, method='sha256'), manager=manager)

        db_session.add(new_user)
        db_session.commit()

        flash('User has been successfully created!', 'success')
        return redirect('/')
    else:
        return render_template('signup.html', isNotLogin=False)


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html', isNotLogin=True)
    elif request.method == 'POST' and 'updateUser' in request.form:
        user_to_update = User.query.get(request.form.get('id'))

        # check if a user already exists wth the new emailù
        user_exists = User.query.filter_by(
            email=request.form.get('email')).first()

        app.logger.info(user_exists)

        if user_exists and user_exists.id != current_user.id:  # if user is found --> redirect to Profile
            flash('Email already exists', 'error')
            return redirect(url_for('profile'))

        user_to_update.name = request.form.get('name')
        user_to_update.surname = request.form.get('surname')
        user_to_update.email = request.form.get('email')
        user_to_update.manager = request.form.get('manager', type=bool)

        if user_to_update.manager == None:
            user_to_update.manager = 0

        db_session.commit()

        flash('User info updated!', 'success')
        return redirect(url_for('profile'))

    elif request.method == 'POST' and 'deleteUser' in request.form:
        User.query.filter_by(id=request.form.get('id')).delete()
        db_session.commit()

        flash('User has been successfully deleted', 'success')
        return redirect('/')

    elif request.method == 'POST' and 'updatePw' in request.form:
        current_password = request.form.get('cur-password')
        new_password = request.form.get('new-password')

        # Current id user
        user_to_update = User.query.get(request.form.get('id'))

        # If current password is wrong
        if not check_password_hash(user_to_update.password, current_password):
            flash('Wrong password, try again.', 'error-pw')
            return redirect(url_for('profile'))

        user_to_update.password = generate_password_hash(
            new_password, method='sha256')

        db_session.commit()

        flash('Password has been successfully updated!', 'success-pw')
        return redirect(url_for('profile'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/sprint', methods=['POST', 'GET'])
@login_required
def sprint():
    if request.method == 'GET':
        current_sprint = Sprint.query.filter_by(
            is_active=1).first()
        if current_sprint != None:
            sprint_tasks = Task.query.filter_by(
                sprint=current_sprint.id).order_by(Task.status)
        else:
            sprint_tasks = None

        return render_template('sprint.html', current_sprint=current_sprint, sprint_task=sprint_tasks, isNotLogin=True)
    elif request.method == 'POST':
        required_data = ['subtask_id', 'new_status']
        # Check data
        for data in required_data:
            if request.form.get(data) == None:
                return 'missing ' + data, 400

        subtask = SubTask.query.get(int(request.form.get('subtask_id')))
        subtask.status = request.form.get('new_status')
        db_session.commit()
        return "success", 200


@app.route('/backlog', methods=['POST', 'GET'])
@login_required
def backlog():
    if request.method == 'GET':
        developer = User.query.filter(User.manager == 0, User.id != 0).all()
        S = aliased(User)  # signaler
        M = aliased(User)  # monitorer

        tasks = db_session.query(Task.id.label("id"), Task.name.label("name"), Task.description.label("description"), Task.sprint.label("sprint"), Task.monitorer.label("monitorer"), Task.signaler.label(
            "signaler"), Task.epic.label("epic"), Task.fibonacci_points.label("fibonacci_points"), Task.status.label("status"), Epic.name.label("epic_name"), Epic.color.label("epic_color"), M.name.label("monitorer_name"), M.surname.label("monitorer_surname"), S.name.label("signaler_name"), S.surname.label("signaler_surname"))\
            .join(Epic, Task.epic == Epic.id)\
            .join(S, Task.signaler == S.id)\
            .join(M, Task.monitorer == M.id)

        current_sprint = db_session.query(Sprint).filter(
            Sprint.is_active == 1).first()
        is_closable = 1
        days_remaning = 0
        today = date.today()
        if current_sprint != None:
            sprint_task = Task.query.filter_by(
                sprint=current_sprint.id).order_by(Task.status)
            current_sprint_id = current_sprint.id

            sprint_task = db_session.query(Task.id.label("id"), Task.name.label("name"), Task.description.label("description"), Task.sprint.label("sprint"), Task.monitorer.label("monitorer"), Task.signaler.label(
                "signaler"), Task.epic.label("epic"), Task.fibonacci_points.label("fibonacci_points"), Task.status.label("status"), Epic.name.label("epic_name"), Epic.color.label("epic_color"), M.name.label("monitorer_name"), M.surname.label("monitorer_surname"), S.name.label("signaler_name"), S.surname.label("signaler_surname"))\
                .filter(Task.sprint == current_sprint_id)\
                .join(Epic, Task.epic == Epic.id)\
                .join(S, Task.signaler == S.id)\
                .join(M, Task.monitorer == M.id)\
                .order_by(Task.status).all()

            task_in_sprint_done = Task.query.filter_by(
                sprint=current_sprint.id, status='DONE').count()
            days_remaning = abs(current_sprint.end_date - today).days
            if task_in_sprint_done == len(sprint_task) and len(sprint_task) != 0:
                is_closable = 0
        else:
            sprint_task = None

        backlog_task = db_session.query(Task.id.label("id"), Task.name.label("name"), Task.description.label("description"), Task.sprint.label("sprint"), Task.monitorer.label("monitorer"), Task.signaler.label(
            "signaler"), Task.epic.label("epic"), Task.fibonacci_points.label("fibonacci_points"), Task.status.label("status"), Epic.name.label("epic_name"), Epic.color.label("epic_color"), M.name.label("monitorer_name"), M.surname.label("monitorer_surname"), S.name.label("signaler_name"), S.surname.label("signaler_surname"))\
            .filter(Task.sprint == None)\
            .join(Epic, Task.epic == Epic.id)\
            .join(S, Task.signaler == S.id)\
            .join(M, Task.monitorer == M.id)\
            .order_by(Task.status)

        epics = Epic.query.filter(Epic.id != 0).all()
        total_points_of_sprint = 100  # Fare SUM di sprint_task.fibonacci_points
        subtasks = SubTask.query.all()
        return render_template('backlog.html', subtasks=subtasks, tasks=tasks, current_sprint=current_sprint, backlog_task=backlog_task, sprint_task=sprint_task, epics=epics, total_points_of_sprint=total_points_of_sprint, is_closable=is_closable, today=today, days_remaning=days_remaning, developer=developer, isNotLogin=True)
    if request.method == 'POST' and 'create-new-task' in request.form:
        # add new task
        new_task = Task(request.form.get('name'),               # name
                        request.form.get('description'),        # description
                        None,                                   # sprint
                        0,                                      # monitorer
                        request.form.get('epic'),               # epic
                        request.form.get('signaler'),           # signaler
                        request.form.get('fibonacci_points'),   # f. points
                        'TODO')                                 # status
        db_session.add(new_task)
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'task-delete' in request.form:
        # delete task
        app.logger.info("DELETE TASK")
        Task.query.filter_by(id=request.form.get('idTask')).delete()
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'task-changed' in request.form:
        # changed task
        app.logger.info("CHANGE TASK")
        task_to_change = Task.query.get(request.form.get('idTask'))
        task_to_change.name = request.form.get('name')
        task_to_change.description = request.form.get('description')
        task_to_change.monitorer = request.form.get('monitorer')
        task_to_change.epic = request.form.get('epic')
        task_to_change.fibonacci_points = request.form.get('fibonacci_points')
        task_to_change.status = request.form.get('status')
        task_to_change.fibonacci_points = request.form.get(
            'fibonacci_points')
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'remove-from-sprint' in request.form:
        # Remove task from sprint
        app.logger.info("REMOVE TASK FROM SPRINT")
        task_to_remove = Task.query.get(request.form.get('idTask'))
        task_to_remove.sprint = None
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'task-move-in-sprint' in request.form:
        # move task in current sprint
        app.logger.info("MOVE TASK IN CURRENT SPRINT")
        task_to_move = Task.query.get(request.form.get('idTask'))
        current_sprint = Sprint.query.filter_by(is_active=1).one()
        task_to_move.sprint = current_sprint.id
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'close-sprint' in request.form:
        app.logger.info("CLOSE SPRINT")
        current_sprint = Sprint.query.filter_by(is_active=1).one()
        sprint_task = Task.query.filter_by(
            sprint=current_sprint.id).update(dict(status='DONE'))
        current_sprint.is_active = 0
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'create-sprint' in request.form:
        app.logger.info("CREATE SPRINT")
        date_start = datetime.date(2022, 6, 1)  # da modificare
        date_end = datetime.date(2022, 6, 30)  # da modificare
        new_sprint = Sprint(request.form.get('name'),
                            date_start,
                            date_end,
                            1)
        db_session.add(new_sprint)
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'update-sprint' in request.form:
        app.logger.info("UPDATE SPRINT")
        current_sprint = Sprint.query.filter_by(is_active=1).one()
        current_sprint.name = request.form.get('name')
        current_sprint.start_date = datetime.date(2022, 6, 1)  # da modificare
        current_sprint.end_date = datetime.date(2022, 6, 30)  # da modificare
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'create-new-epic' in request.form:
        app.logger.info("NEW EPIC")
        new_epic = Epic(request.form.get('name'),
                        request.form.get('description'),
                        request.form.get('color'))
        db_session.add(new_epic)
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'modal-move-task' in request.form:
        task_to_move = Task.query.get(request.form.get('idTaskToMove'))
        in_sprint = request.form.get('in_sprint')
        if int(in_sprint) == 0:  # da backlog a sprint
            current_sprint = Sprint.query.filter_by(is_active=1).one()
            task_to_move.sprint = current_sprint.id
        else:  # da sprint a backlog
            task_to_move.sprint = None
        db_session.commit()
    if request.method == 'POST' and 'create-new-subtask' in request.form:
        app.logger.info("Create new subtask")
        father_task = request.form.get('father_task')
        name = request.form.get('name')
        description = request.form.get('description')
        assigned_to = request.form.get('assigned_to')
        new_subtask = SubTask(name, description, father_task, assigned_to)
        db_session.add(new_subtask)
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'move_task' in request.form:
        required_data = ['task_id', 'new_status']
        # Check data
        for data in required_data:
            if request.form.get(data) == None:
                return 'missing ' + data, 400
        task = Task.query.get(int(request.form.get('task_id')))
        if request.form.get('new_status') == '-1':
            task.sprint = None
        else:
            task.sprint = request.form.get('new_status')
        db_session.commit()
        return "success", 200

    # Close connection to database when shutting down
    shutdown_session()


@app.route('/epics', methods=['POST', 'GET'])
@login_required
def epics():
    if request.method == 'GET':
        app.logger.info("EPICS")
        epics = db_session.query(Epic).filter(Epic.id != 0).all()
        tasks_with_epic = db_session.query(Task).filter(
            Task.epic != 0, Task.status != 'DONE').all()
        return render_template('epics.html', epics=epics, tasks_with_epic=tasks_with_epic, isNotLogin=True)
    if request.method == 'POST' and 'create-new-epic' in request.form:
        app.logger.info("NEW EPIC")
        new_epic = Epic(request.form.get('name'),
                        request.form.get('description'),
                        request.form.get('color'))
        db_session.add(new_epic)
        db_session.commit()
        return redirect('/epics')


@ app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
