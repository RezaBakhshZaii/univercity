import sqlite3


def connection_create_table():
    try:
        con = sqlite3.Connection("informationdb.db")
        sql = con.cursor()
        sql.execute(
            "CREATE TABLE IF NOT EXISTS student(userid INTEGER PRIMARY KEY,username INTEGER,password TEXT,name TEXT,"
            "reshte TEXT,dore TEXT,moadel TEXT,phone TEXT,meli TEXT,image BLOB NOT NULL)")
        sql.execute(
            "CREATE TABLE IF NOT EXISTS photos(username INTEGER PRIMARY KEY,pickclass BLOB NOT NULL,pickexam BLOB NOT "
            "NULL,pickpresence BLOB NOT NULL,picknumber BLOB NOT NULL,pickok BLOB NOT NULL)")
        con.close()
        return 1
    except:
        con.close()
        return 0


def connection_create_food():
    con = sqlite3.Connection("fooddb.db")
    sql = con.cursor()
    try:
        sql.execute(
            "CREATE TABLE IF NOT EXISTS food(userid INTEGER PRIMARY KEY,username INTEGER,password TEXT,name TEXT)")
        con.close()
        return 1
    except:
        con.close()
        return 0


def add_food(data):
    con = sqlite3.Connection("fooddb.db")
    sql = con.cursor()
    try:
        sql.executemany("INSERT INTO food VALUES (?,?,?,?)", data)
        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        con.close()
        return 0


def get_food(userid):
    con = sqlite3.Connection("fooddb.db")
    sql = con.cursor()
    try:
        user = sql.execute("SELECT * FROM food WHERE userid=(?)", (userid,))
        user = user.fetchone()
        con.close()
        return user
    except:
        con.close()
        return 0


def get_food_name(username):
    con = sqlite3.Connection("fooddb.db")
    sql = con.cursor()
    try:
        user = sql.execute("SELECT * FROM food WHERE username=(?)", (username,))
        user = user.fetchone()
        con.close()
        return user
    except:
        con.close()
        return 0


def delete_food(username):
    con = sqlite3.Connection("fooddb.db")
    sql = con.cursor()
    try:
        sql.execute("DELETE FROM food WHERE username=(?)", (username,))
        con.commit()
        con.close()
        return 1
    except:
        con.close()
        return 0


def add_student(data: object) -> object:
    con = sqlite3.Connection("informationdb.db")
    sql = con.cursor()
    try:
        sql.executemany("INSERT INTO student VALUES (?,?,?,?,?,?,?,?,?,?)", data)
        con.commit()
        con.close()
        return 1
    except:
        con.close()
        return 0


def add_photos(data):
    con = sqlite3.Connection("informationdb.db")
    sql = con.cursor()
    try:
        sql.executemany("INSERT INTO photos VALUES (?,?,?,?,?,?)", data)
        con.commit()
        con.close()
        return 1
    except:
        con.close()
        return 0


def get_photos(username):
    con = sqlite3.Connection("informationdb.db")
    sql = con.cursor()
    try:
        user = sql.execute("SELECT * FROM photos WHERE username=(?)", (username,))
        user = user.fetchone()
        con.close()
        return user
    except:
        con.close()
        return 0


def get_information_id(userid):
    con = sqlite3.Connection("informationdb.db")
    sql = con.cursor()
    try:
        user = sql.execute("SELECT * FROM student WHERE userid=(?)", (userid,))
        user = user.fetchone()
        con.close()
        return user
    except:
        con.close()
        return 0


def get_information_username(username):
    con = sqlite3.Connection("informationdb.db")
    sql = con.cursor()
    try:
        user = sql.execute("SELECT * FROM student WHERE username=(?)", (username,))
        user = user.fetchone()
        con.close()
        return user
    except:
        con.close()
        return 0


def delete_student(username):
    con = sqlite3.Connection("informationdb.db")
    sql = con.cursor()
    try:
        sql.execute("DELETE FROM student WHERE username=(?)", (username,))
        con.commit()
        con.close()
        return 1
    except:
        con.close()
        return 0


def delete_photo(username):
    con = sqlite3.Connection("informationdb.db")
    sql = con.cursor()
    try:
        sql.execute("DELETE FROM photos WHERE username=(?)", (username,))
        con.commit()
        con.close()
        return 1
    except:
        con.close()
        return 0

