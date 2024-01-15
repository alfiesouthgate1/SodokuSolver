import sqlite3
from sqlite3 import Error
from config import db_file
def initialize_database():
    sql = """CREATE TABLE IF NOT EXISTS user (email VARCHAR(20), password VARCHAR(20), PRIMARY KEY (email));"""
    run_query(sql)
def create_user(email, pwd, dbfile):
    print("called with values:", email, pwd)
    try:
        sql = f"""INSERT INTO user (email, password) VALUES ('{email}', '{pwd}');"""
        run_query(sql, dbfile)
    except sqlite3.Error as e:
        raise ValueError("Email already in use")

def get_user(email):
    sql = f"""SELECT * FROM user WHERE email == email"""
    x = run_query(sql)
    return x

def update_user(email, pwd, new_pwd):
    if pwd == get_user(email)[0][1]:
        try:
            sql = f"""UPDATE user Set password = ('{new_pwd}') WHERE email == email"""
            run_query(sql)
        except sqlite3.Error as e:
            raise e
    else:
        print("wrong password")

def remove_user(email, pwd):
    if pwd == get_user(email)[0][1]:
        try:
            sql = f"""DELETE FROM user WHERE email == email"""
            run_query(sql)
        except sqlite3.Error as e:
            raise ""


def delete_table():
    sql = f"""DELETE FROM user"""
    try:
        run_query(sql)
    except sqlite3.Error as e:
        raise e
def run_query(query, dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        print("executing query:", query)
        cursor.execute(query)
        conn.commit()
        print("worked")
        return cursor.fetchall()

    except sqlite3.Error as e:
        raise e
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_user("wjdi@djijd.com", "djijd", db_file)

