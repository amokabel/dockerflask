from flask import Flask
import mysql.connector
import sys

class Database:
    def __init__(self, password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user='root', 
            password=pf.read(),
            host='db',
            database='testdb',
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()

    def addEntry(self, msg):
        self.cursor.execute("INSERT INTO messages (msg) VALUES('%s');" %msg)

app = Flask(__name__)
g_conn = None

def db_handle():
    global g_conn
    if not g_conn:
        try: 
            g_conn = Database('/run/secrets/db-password')
        except mysql.connector.errors.ProgrammingError as e:
            print(e.msg)
            g_conn = None

    return g_conn


@app.route('/')
def index():
    conn = db_handle()
    if conn:
        db_handle().addEntry("hello")

    return "Hello"

