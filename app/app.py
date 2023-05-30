from flask import Flask
import mysql.connector
import sys
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
g_conn = None

class Database:
    def __init__(self, password_file):
        app.logger.info("Connecting to db")
        with open(password_file, 'r', newline='') as pf:
            pwd = pf.read().rstrip('\n')

            self.connection = mysql.connector.connect(
                user='root', 
                password=pwd,
                host='db',
                database='testdb',
                auth_plugin='mysql_native_password'
            )
            self.cursor = self.connection.cursor()

    def addEntry(self, msg):
        app.logger.info("Adding entry: %s" %msg)
        self.cursor.execute("INSERT INTO messages (msg) VALUES('%s');" %msg)

    def fetchEntries(self):
        app.logger.info("Fetching entries")
        ret = []
        self.cursor.execute("SELECT msg, ts FROM messages;")
        for c in self.cursor:
            ret.append(c[0])

        return ret

def db_handle():
    global g_conn
    if not g_conn:
        try: 
            g_conn = Database('/var/run/secrets/db-password')
        except mysql.connector.errors.ProgrammingError as e:
            app.logger.error(e.msg)
            g_conn = None

    return g_conn


@app.route('/')
def index():
    conn = db_handle()
    entries = []
    if conn:
        db_handle().addEntry("hello")
        messages = db_handle().fetchEntries()
    else:
        app.logger.error("Could not add entry")

    msg = "Disco\n"
    for m in messages:
        msg += m
        msg += '\n'

    return msg

