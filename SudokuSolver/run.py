from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, session
from db import create_user, run_query, get_user, update_user, remove_user
from config import db_file
from solver import solve_grid, is_valid, find_empty_cell
from generator import generate_grid, easy, medium, hard
import random
import string
app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.secret_key = ''.join(random.choices(string.ascii_letters, k=32))
#HomePage
@app.route('/')
def home():
    return render_template('index.html')
#SignUpPage
@app.route('/signup')
def signup():
    return render_template('signup.html')
# Get Data from Signup into database
@app.route('/signup1', methods = ['POST', 'GET'])
def signup1():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = create_user(email, password, db_file)
        if result[0]:
            session['email'] = email
            return redirect(url_for('choice'))
        else:
            error_msg = result[1]
            return render_template('signup.html', error_msg=error_msg)
#LoginPage
@app.route('/login')
def login():
    return render_template('login.html')
#Check if Login data is in database
@app.route('/login1', methods = ['POST', 'GET'])
def login1():
    print("called")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = get_user(email, password, db_file)
        if not result:
            error_msg = "Incorrect Email or Password"
            return render_template('login.html', error_msg=error_msg)
        else:
            session['email'] = email
            return redirect(url_for('choice'))
# Change Password Page
@app.route('/changepassword')
def change_password():
    return render_template('change_password.html')
# Update Database
@app.route('/changepassword1', methods=['POST', 'GET'])
def changepassword1():
    print("called")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        new_pwd = request.form['newpassword']
        result = update_user(email, password, new_pwd, db_file)
        if result:
            return redirect(url_for('home'))
        else:
            error_msg = "Incorrect Email or Password"
            return render_template('change_password.html', error_msg=error_msg)
# Delete Account Page
@app.route('/deleteaccount')
def deleteaccount():
    return render_template('deleteaccount.html')
#Delete data from database
@app.route('/deleteaccount1', methods=['POST', 'GET'])
def deleteaccount1():
    print("called")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = remove_user(email, password, db_file)
        if not result:
            error_msg = "Incorrect Email or Password"
            return render_template('deleteaccount.html', error_msg=error_msg)
        else:
            return redirect(url_for('home'))
# Choice Page
@app.route('/choice')
def choice():
    if 'email' in session:
        return render_template("choice.html")
    else:
        return redirect(url_for('home'))
# Load Sudoku Solver Page
@app.route('/sudokusolver')
def sudoku_solver():
    if 'email' in session:
        return render_template('solver.html')
    else:
        return redirect(url_for('home'))
# Solve the board to pass to frontend
@app.route('/solve', methods=['POST', 'GET'])
def solve():
    data = request.json
    sudokugrid = data.get('grid') #Get grid from frontend
    result = solve_grid(sudokugrid, False)
    if result is None:
        error_msg = "This is unsolvable"
        return jsonify({"error_msg": error_msg})
    else:
        sudokugrid = solve_grid(sudokugrid, False)
        return jsonify(sudokugrid)
# Play Sudoku Page
@app.route('/play')
def play():
    difficulty = request.args.get('difficulty') #Get Difficulty from previous page
    return render_template('play_sudoku.html', difficulty=difficulty)
# Pass Sudoku Grid to frontend
@app.route('/playsudoku', methods=['POST'])
def playsudoku():
    data = request.json
    sudokugrid = data.get('grid') #Get Grid from frontend
    e_m_h = data.get('difficulty') #Get difficulty from frontend
    difficulty_levels = {'1': 1, '2': 2, '3': 3}
    difficulty = difficulty_levels.get(e_m_h)
    if difficulty is not None:
        sudokugrid = generate_grid(sudokugrid)
        if difficulty == 1:
            sudokugrid = easy(sudokugrid)
        elif difficulty == 2:
            sudokugrid = medium(sudokugrid)
        elif difficulty == 3:
            sudokugrid = hard(sudokugrid)
        return jsonify(sudokugrid)
    else:
        return jsonify({'error': 'Invalid difficulty level'}), 400
#Difficulty Page
@app.route('/difficulty')
def difficulty():
    if 'email' in session:
        return render_template('e_m_h.html')
    else:
        return redirect(url_for('home'))
#Logout Route
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
