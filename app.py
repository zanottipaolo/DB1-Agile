from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('login.html')

@app.route('/sprint', methods=['POST', 'GET'])
def sprint():
    return render_template('sprint.html')

if __name__ == '__main__': 
     app.run(debug=True)