import mysql.connector
from project2 import connect_proj2

# connect to the database of employees and their hashed passwords

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect_proj2.dbuser, \
    password=connect_proj2.dbpass, host=connect_proj2.dbhost, \
    port=connect_proj2.dbport, \
    database=connect_proj2.dbname, autocommit=True)
    dbconn = connection.cursor(buffered=True)
    return dbconn
