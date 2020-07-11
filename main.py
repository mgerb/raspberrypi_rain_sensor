from flask import Flask, g
from gpiozero import Button
import sqlite3
import threading
import time
import datetime

gpioPin = 18
app = Flask(__name__)

DATABASE = './database.db'


def get_db() -> sqlite3.Connection:
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def query_dates() -> str:
    data = query_db(
        "select date(timestamp, 'unixepoch') as date, count(*) as count from rain_sensor group by date(timestamp, 'unixepoch')")
    out = "<table><thead><th>Date</th><th>Count</th></thead><tbody>"

    for d in data:
        out += "<tr><td>" + d[0] + "</td><td>" + str(d[1]) + "</td></tr>"

    out += "</tbody></table>"
    return out


@app.route('/')
def base_route():
    return query_dates()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()


# unix timestamp input
def insert_date(date: int):
    with app.app_context():
        conn = get_db()
        conn.execute(
            "INSERT INTO rain_sensor (timestamp) VALUES (?);", (date,))
        conn.commit()
        conn.close()


def rain_sensor_task():
    button = Button(gpioPin)
    while True:
        if button.is_pressed:
            insert_date(int(datetime.datetime.utcnow().timestamp()))
            time.sleep(5)
        time.sleep(0.01)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    init_db()
    threading.Thread(target=rain_sensor_task).start()
    app.run(host="0.0.0.0", port=8080)
