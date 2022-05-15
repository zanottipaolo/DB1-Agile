from flask import Flask, redirect, render_template, request

# Database
from backend.database import db_session

# Models
from backend.models import Sprint, Task

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
        return render_template('backlog/backlog.html',tasks=tasks)
    else:
        # add new task
        new_task = Task(request.form.get('name'), request.form.get('description'))
        db_session.add(new_task)
        db_session.commit()
        return redirect('/backlog')

# Close connection to database when shutting down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__': 
     app.run(debug=True)