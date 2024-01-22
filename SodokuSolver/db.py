import sqlite3
from sqlite3 import Error
from config import db_file
import re
def initialize_database(db_file):
    sql = """CREATE TABLE IF NOT EXISTS user (email VARCHAR(20), password VARCHAR(20), PRIMARY KEY (email));"""
    run_query(sql, db_file)
def create_user(email, pwd, dbfile):
    print("called with values:", email, pwd)
    if valid_email(email):
        if valid_password(pwd):
            try:
                sql = f"""INSERT INTO user (email, password) VALUES ('{email}', '{pwd}');"""
                run_query(sql, dbfile)
                return [True, ""]
            except sqlite3.Error as e:
                return [False, "Email already in use"]
        else:
            return [False, "Password requires at least one letter and number and must be at least 8 characters"]
    else:
        return [False, "Invalid Email"]

def get_user(email, pwd, dbfile):
    try:
        sql = f"""SELECT * FROM user WHERE email = ? AND password = ?"""
        result = run_query(sql, dbfile, (email, pwd))
        return result
    except sqlite3.Error as e:
        raise ValueError("didn't work")

def update_user(email, pwd, new_pwd, dbfile):
    user_data = get_user(email, pwd, dbfile)
    if user_data and len(user_data) > 0 :
        if pwd == user_data[0][1]:
            try:
                sql = f"""UPDATE user Set password = ? WHERE email = ?"""
                result = run_query(sql, dbfile, (new_pwd, email))
                return True
            except sqlite3.Error as e:
                raise e
        else:
            return False
    else:
        return False

def remove_user(email, pwd, dbfile):
    user_data = get_user(email, pwd, dbfile)
    if user_data and len(user_data) > 0:
        if pwd == user_data[0][1]:
            try:
                sql = f"""DELETE FROM user WHERE email = ?"""
                run_query(sql, dbfile, (email,))
                return True
            except sqlite3.Error as e:
                raise ""
        else:
            return False
    else:
        return False


def delete_table():
    sql = f"""DELETE FROM user"""
    try:
        run_query(sql)
    except sqlite3.Error as e:
        raise e
def run_query(query, dbfile, params=None):
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        print("executing query:", query)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        print("worked")
        return cursor.fetchall()

    except sqlite3.Error as e:
        raise e
        conn.rollback()
    finally:
        conn.close()
def valid_email(email):
    match = re.search(r'[\w.-]+@[\w.-]+.\w+', email)
    if match:
        return True
    else:
        return False
def valid_password(password):
    match = re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password)
    if match:
        return True
    else:
        return False


if __name__ == "__main__":
    create_user("susif9i9@mail.com", "fhfu", db_file)



