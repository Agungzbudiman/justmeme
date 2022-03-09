import sqlite3

from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('mydatabase.db')

        return con

    except Error:

        print(Error)

def sql_table_group_join(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE group_join(id integer PRIMARY KEY, user_id integer, group_id integer)")

    con.commit()

def sql_table_group_start(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE group_start(id integer PRIMARY KEY, game_start integer, group_id integer)")

    con.commit()


def sql_table_jawaban(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE group_jawaban(id integer PRIMARY KEY, user_id integer, group_id integer, jawaban text)")

    con.commit()

con = sql_connection()

sql_table_jawaban(con)