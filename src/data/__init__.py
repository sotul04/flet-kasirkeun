import sqlite3

def getConnection(database : str = "my-flet-app/data/KasirkeunData.db"):
    conn = sqlite3.connect(database, check_same_thread=False)
    return conn, conn.cursor()

def commit():
    connection.commit()

def close():
    connection.close()

connection, cursor = getConnection()