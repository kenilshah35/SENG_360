#!/usr/bin/python3
"""Server for async chat application"""

"""
Last edited by   : Ella
Last edited time : 12/4/2021
"""
from mysql.connector import connect

def login_verification(username, password):
    """ lookup if credentials are in the database """ 
    db = connect(
        database='dev',
        host='localhost',
        user='server',
        password='tomato',
        auth_plugin='mysql_native_password',
    )
    cursor = db.cursor()
    sql = ("SELECT * FROM credentials WHERE username =%s AND password =%s")
    cursor.execute(sql,(username, password))
    results = cursor.fetchall()
    if results:
        if results[0][3] == 0:
            # the account is locked
            return "LOCKED"
        return "VALID"
    return "INVALID"

def lock_account(username):
    """ locks account with given username. """
    db = connect(
        database='dev',
        host='localhost',
        user='server',
        password='tomato',
        auth_plugin='mysql_native_password',
    )
    cursor = db.cursor()
    # set active attribute on account to 0. 
    # active must then be manually updated via the container to unlock the account.
    sql = ("UPDATE credentials SET active =0 WHERE username =%s")
    cursor.execute(sql, (username,))
    db.commit()

def delete_account(username):
    """ Deletes account. """
    db = connect(
        database='dev',
        host='localhost',
        user='server',
        password='tomato',
        auth_plugin='mysql_native_password',
    )
    cursor = db.cursor()
    sql = ("DELETE FROM credentials WHERE username =%s")
    cursor.execute(sql, (username,))
    db.commit()

def check_account(username):
    """ Checks if account exists. """
    db = connect(
        database='dev',
        host='localhost',
        user='server',
        password='tomato',
        auth_plugin='mysql_native_password',
    )
    cursor = db.cursor()
    sql = ("SELECT * FROM credentials WHERE username =%s")
    cursor.execute(sql,(username,))
    results = cursor.fetchall()
    if results:
        return True
    return False

def add_account(username, password):
    """ Creates account with given username and password. """
    db = connect(
        database='dev',
        host='localhost',
        user='server',
        password='tomato',
        auth_plugin='mysql_native_password',
    )
    cursor = db.cursor()
    sql = ("INSERT INTO credentials (username, password, active) VALUES (%s, %s, 1);")
    cursor.execute(sql, (username, password))
    db.commit()
