from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, session
from db import create_user, run_query, get_user, update_user, remove_user
from config import db_file
from solver import solve_grid, is_valid, find_empty_cell
from generator import generate_grid, easy, medium, hard
app = Flask(__name__)
app.secret_key = 'sudukoALFIE123'
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

@app.route('/sudokusolver')
def sudoku_solver():
    return render_template('solver.html')
@app.route('/solve', methods=['POST', 'GET'])
def solve():
    data = request.json
    sudokugrid = data.get('grid')
    result = solve_grid(sudokugrid, False)
    if result is None:
        error_msg = "This is unsolvable"
        print(error_msg)
        return jsonify({"error_msg": error_msg})
    else:
        sudokugrid = solve_grid(sudokugrid, False)
        return jsonify(sudokugrid)

@app.route('/play')
def play():
    difficulty = request.args.get('difficulty')
    return render_template('play_sudoku.html', difficulty=difficulty)
@app.route('/playsudoku', methods=['POST'])
def playsudoku():
    data = request.json
    print(data)
    sudokugrid = data.get('grid')
    e_m_h = data.get('difficulty')

    # Convert difficulty string to corresponding integer value
    difficulty_levels = {'1': 1, '2': 2, '3': 3}
    difficulty = difficulty_levels.get(e_m_h)

    if difficulty is not None:
        sudokugrid = generate_grid(sudokugrid)  # Assuming this function prepares the Sudoku grid

        if difficulty == 1:
            sudokugrid = easy(sudokugrid)
        elif difficulty == 2:
            sudokugrid = medium(sudokugrid)
        elif difficulty == 3:
            sudokugrid = hard(sudokugrid)

        return jsonify(sudokugrid)
    else:
        return jsonify({'error': 'Invalid difficulty level'}), 400
@app.route('/difficulty')
def difficulty():
    return render_template('e_m_h.html')


if __name__ == '__main__':
    app.run()
