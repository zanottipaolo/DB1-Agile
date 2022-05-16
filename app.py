from datetime import date
import datetime
from time import strptime
from webbrowser import get
from flask import Flask, redirect, render_template, request
from sqlalchemy import desc

# Database
from backend.database import db_session

# Models
from backend.models import Sprint, Task, Epic

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/sprint', methods=['POST', 'GET'])
def sprint():
    if request.method == 'GET':
        tasks = Task.query.all()
        sprints = Sprint.query.all()
        current_sprint = Sprint.query.filter_by(
            is_active=1).first()
        if current_sprint != None:
            sprint_task = Task.query.filter_by(
                sprint=current_sprint.id).order_by(Task.status)
        else:
            sprint_task = None
        return render_template('sprint.html', tasks=tasks, sprints=sprints, current_sprint=current_sprint, sprint_task=sprint_task)


@app.route('/backlog', methods=['POST', 'GET'])
def backlog():
    if request.method == 'GET':
        tasks = Task.query.all()
        sprints = Sprint.query.all()
        current_sprint = Sprint.query.filter_by(
            is_active=1).first()
        is_closable = 1
        days_remaning = 0
        today = date.today()
        if current_sprint != None:
            sprint_task = Task.query.filter_by(
                sprint=current_sprint.id).order_by(Task.status)
            task_in_sprint_done = Task.query.filter_by(
                sprint=current_sprint.id, status='DONE').count()
            days_remaning = abs(current_sprint.end_date - today).days
            if task_in_sprint_done == sprint_task.count() and sprint_task.count() != 0:
                is_closable = 0
        else:
            sprint_task = None

        backlog_task = Task.query.filter_by(
            sprint=None).order_by(Task.status)
        epics = Epic.query.all()
        total_points_of_sprint = 100  # Fare SUM di sprint_task.fibonacci_points
        return render_template('backlog/backlog.html', tasks=tasks, sprints=sprints, current_sprint=current_sprint, backlog_task=backlog_task, sprint_task=sprint_task, epics=epics, total_points_of_sprint=total_points_of_sprint, is_closable=is_closable, today=today, days_remaning=days_remaning)
    if request.method == 'POST' and 'create-new-task' in request.form:
        # add new task
        new_task = Task(request.form.get('name'),
                        request.form.get('description'),
                        None,
                        None,
                        request.form.get('epic'),
                        request.form.get('signaler'),
                        request.form.get('fibonacci_points'),
                        'TODO')
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
        task_to_change.status = request.form.get('status')
        # reporter
        task_to_change.fibonacci_points = request.form.get(
            'fibonacci_points_info')
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
    # Close connection to database when shutting down


@ app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
