import os
import sys
import sqlite3


def getbasefile():
    """Name of the SQLite DB file"""
    return os.path.splitext(os.path.basename(__file__))[0]


def connectdb():
    """Connect to the SQLite DB"""
    try:
        dbfile = getbasefile() + '.db'
        conn = sqlite3.connect(dbfile, timeout=2)
    except BaseException as err:
        print(str(err))
        conn = None
    return conn


def corecursor(conn, query, args):
    """Opens a SQLite DB cursor"""
    result = False
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        rows = cursor.fetchall()
        numrows = len(list(rows))
        if numrows > 0:
            result = True
    except sqlite3.OperationalError as err:
        print(str(err))
        if cursor is not None:
            cursor.close()
    finally:
        if cursor is not None:
            cursor.close()
    return result


def tableexists(table):
    """Checks if a SQLite DB Table exists"""
    result = False
    conn = connectdb()
    try:
        if not conn is None:
            qry = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
            args = (table,)
            result = corecursor(conn, qry, args)
            if conn is not None:
                conn.close()
    except sqlite3.OperationalError as err:
        print(str(err))
        if conn is not None:
            conn.close()
    return result


conn = connectdb()

cursor_ = conn.cursor()
TABLE = 'register'
cursor_.execute(f"CREATE TABLE {TABLE}( name text, phone text, address text )")
conn.commit()

if tableexists(TABLE):
    print(f"Table '{TABLE}' exists")

conn.close()
