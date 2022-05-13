from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/sprint', methods=['POST', 'GET'])
def sprint():
    return render_template('sprint.html')

if __name__ == '__main__': 
     app.run(debug=True)