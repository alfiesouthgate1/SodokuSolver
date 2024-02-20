from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from db import create_user, run_query, get_user, update_user, remove_user
from config import db_file

app = Flask(__name__)
#HomePage
@app.route('/')
def hello_world():
    return render_template('index.html')
#SignUpPage
@app.route('/signup')
def signup():
    return render_template('signup.html')
#LoginPage
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/success')
def success():
    return render_template("success.html")
# Get Data from Signup into database
@app.route('/submit', methods = ['POST', 'GET'])
def submit():
    print("called")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = create_user(email, password, db_file)
        if result[0]:
            return redirect(url_for('success'))
        else:
            error_msg = result[1]
            return render_template('signup.html', error_msg=error_msg)
        print("user created successfully")
        sql = """SELECT * FROM user"""
        print(run_query(sql, db_file))
        return redirect(url_for('success'))
#Check if Login data is in database
@app.route('/submit1', methods = ['POST', 'GET'])
def submit1():
    print("called")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        y = get_user(email, password, db_file)
        if not y:
            error_msg = "Incorrect Email or Password"
            return render_template('login.html', error_msg=error_msg)
        else:
            return redirect(url_for('success'))
@app.route('/changepassword')
def change_password():
    return render_template('change_password.html')
@app.route('/submit2', methods=['POST', 'GET'])
def submit2():
    print("called")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        new_pwd = request.form['newpassword']
        x = update_user(email, password, new_pwd, db_file)
        if x:
            return redirect(url_for('success'))
        else:
            error_msg = "Incorrect Email or Password"
            return render_template('change_password.html', error_msg=error_msg)
@app.route('/deleteaccount')
def deleteaccount():
    return render_template('deleteaccount.html')
#Delete Account data handling
@app.route('/submit3', methods=['POST', 'GET'])
def submit3():
    print("called")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        x = remove_user(email, password, db_file)

        print(x)
        if not x:
            error_msg = "Incorrect Email or Password"
            return render_template('deleteaccount.html', error_msg=error_msg)
        else:
            return redirect(url_for('success'))
if __name__ == '__main__':
    app.run()
