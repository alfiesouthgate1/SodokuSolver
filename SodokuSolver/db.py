import sqlite3
from sqlite3 import Error



def create_user(email, pwd):
    # conn = None
    try:
        sql = f"""INSERT INTO user (email, password) VALUES ('{email}', '{pwd}');"""
        run_query(sql)
    except sqlite3.Error as e:
        raise e

def get_user(email):
    sql = f"""SELECT * FROM user WHERE email == email"""
    x = run_query(sql)
    return x

def update_user(email, pwd):
    return

def remove_user(email, pwd):
    if pwd == get_user(email)[0][1]:
        try:
            sql = f"""DELETE FROM user WHERE email == email"""
            run_query(sql)
        except sqlite3.Error as e:
            raise e

def delete_table():
    sql = f"""DELETE FROM user"""
    try:
        run_query(sql)
    except sqlite3.Error as e:
        raise e
def run_query(query):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return cursor.fetchall()

    except sqlite3.Error as e:
        raise e
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    db_file = "../identifier.sqlite"
    create_user("alfie@outlook.com", "hello")
    create_user("hd@dd.com", "hi")
    print(get_user("alfie@outlook.com")[0][1])
    remove_user("alfie@outlook.com", "hello")
    print(get_user("alfie@outlook.com"))2