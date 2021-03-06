#!/usr/bin/python3

from datetime import datetime
import os
import glob
import time
import sqlite3

from webui import weather, temperature

DBNAME = "/home/josterpi/raspberrypi/templog.db"

LOCATION_TAG = "lasalle-office"

def get_outside_temp():
    conn = sqlite3.connect(DBNAME)
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS outside (fetched DATETIME, temp NUMERIC)")
    curs.execute("SELECT temp FROM outside WHERE fetched > datetime('now', 'localtime', '-10 minutes')")
    row = curs.fetchone()
    if row is None:
        w = weather.get_weather()
        temp = w['main']['temp']
        curs.execute("INSERT INTO outside VALUES(datetime('now', 'localtime'), (?))", (temp,))
    else:
        temp = row[0]
    conn.commit()
    conn.close()
    return temp

def log_temp(temp):
    conn = sqlite3.connect(DBNAME)
    outside = get_outside_temp()
    scheduled = temperature.scheduled_temp(datetime.now())
    curs = conn.cursor()
    curs.execute("INSERT INTO temps values(datetime('now', 'localtime'), ?, ?, ?, ?)", (temp, outside, scheduled, LOCATION_TAG))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    log_temp(temperature.read_temp())
