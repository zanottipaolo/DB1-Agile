from flask import Flask, render_template

# Database
from backend.database import db_session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

# Close connection to database when shutting down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__': 
     app.run(debug=True)