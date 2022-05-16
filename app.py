from flask import Flask, redirect, render_template, request

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
    sprint = Sprint.query.all()
    return render_template('sprint.html', sprint=sprint)


@app.route('/backlog', methods=['POST', 'GET'])
def backlog():
    if request.method == 'GET':
        tasks = Task.query.all()
        sprints = Sprint.query.all()
        current_sprint = Sprint.query.filter_by(is_active=1).first()
        backlog_task = Task.query.filter_by(sprint=None)
        sprint_task = Task.query.filter_by(sprint=current_sprint.id)
        return render_template('backlog/backlog.html', tasks=tasks, sprints=sprints, current_sprint=current_sprint, backlog_task=backlog_task, sprint_task=sprint_task)
    if request.method == 'POST' and 'create-new-task' in request.form:
        # add new task
        new_task = Task(request.form.get('name'),
                        request.form.get('description'))
        db_session.add(new_task)
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'task-delete' in request.form:
        # delete task
        app.logger.info("DELETE TASK")
        Task.query.filter_by(id=request.form.get('idTaskToDelete')).delete()
        db_session.commit()
        return redirect('/backlog')
    if request.method == 'POST' and 'task-changed' in request.form:
        # delete task
        app.logger.info("CHAGE TASK")
        return redirect('/backlog')
    # Close connection to database when shutting down


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
