import sqlite3
from sqlite3 import Error



def create_user(email, pwd):
    conn = None
    sql = f"""INSERT INTO user (email, password) VALUES ('{email}', '{pwd}');"""
    try:
        conn = sqlite3.connect("../identifier.sqlite")
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)
    return conn

def get_user(email, pwd):
    return

def update_user(email, pwd):
    return

def remove_user(email, pwd):
    return

if __name__ == "__main__":
    create_user("alfie@outlook.com", "hello")
