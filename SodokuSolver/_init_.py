from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import create_user, run_query
from config import db_file

app = Flask(__name__)
@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/success')
def success():
    return render_template("success.html")
# Get Data from Login
@app.route('/submit', methods = ['POST', 'GET'])
def submit():
    print("called")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        create_user(email, password, db_file)
        print("user created successfully")
        print(email, password)
        return redirect(url_for('success'))
if __name__ == '__main__':
    app.run()
