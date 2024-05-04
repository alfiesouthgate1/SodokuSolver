import sqlite3
from sqlite3 import Error
from config import db_file
import re
import hashlib
import os
# Initialise database
def initialize_database(db_file):
    sql = """CREATE TABLE IF NOT EXISTS user (email VARCHAR(20), password VARCHAR(20), PRIMARY KEY (email));"""
    run_query(sql, db_file)
# Create User
def create_user(email, pwd, dbfile):
    if valid_email(email):
        if valid_password(pwd):
            hashed_pwd = hash_password(pwd)
            try:
                sql = f"""INSERT INTO user (email, password) VALUES (?, ?);"""
                run_query(sql, dbfile, (email, hashed_pwd))
                return [True, ""]
            except sqlite3.Error as e:
                return [False, "Email already in use"]
        else:
            return [False, "Password requires at least one letter and number and must be at least 8 characters, Password must not contain special characters"]
    else:
        return [False, "Invalid Email"]
# Get user
def get_user(email, pwd, dbfile):
    try:
        sql = f"""SELECT * FROM user WHERE email = ?"""
        result = run_query(sql, dbfile, (email,))
        if result:
            stored_password = result[0][1]
            if verify_password(stored_password, pwd):
                return result
        return []
    except sqlite3.Error as e:
        raise ValueError("didn't work")

# Update User
def update_user(email, pwd, new_pwd, dbfile):
    user_data = get_user(email, pwd, dbfile)
    if user_data and len(user_data) > 0 :
        stored_password = user_data[0][1]
        if verify_password(stored_password, pwd):
            hashed_new_pwd = hash_password(new_pwd)
            try:
                sql = f"""UPDATE user Set password = ? WHERE email = ?"""
                result = run_query(sql, dbfile, (hashed_new_pwd, email))
                return True
            except sqlite3.Error as e:
                raise e
        else:
            return False
    else:
        return False
# Remove User
def remove_user(email, pwd, dbfile):
    user_data = get_user(email, pwd, dbfile)
    if user_data and len(user_data) > 0:
        stored_password = user_data[0][1]
        if verify_password(stored_password, pwd):
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

# Delete Table
def delete_table():
    sql = f"""DELETE FROM user"""
    try:
        run_query(sql)
    except sqlite3.Error as e:
        raise e
# Function to execute sql queries
def run_query(query, dbfile, params=None):
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.fetchall()

    except sqlite3.Error as e:
        raise e
        conn.rollback()
    finally:
        conn.close()
# Check if email is valid
def valid_email(email):
    match = re.search(r'[\w.-]+@[\w.-]+.\w+', email)
    if match:
        return True
    else:
        return False
# Check if Password is valid
def valid_password(password):
    match = re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password)
    if match:
        return True
    else:
        return False
# Hash password
def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key
# Verify Password
def verify_password(stored_password, provided_password):
    salt = stored_password[:32]
    stored_key = stored_password[32:]
    key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return key == stored_key

if __name__ == "__main__":
    create_user("susi3f9i9@mail.com", "fhfu", db_file)



