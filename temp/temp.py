
import os
import glob
import time
import sqlite3
 
from flask import Flask, render_template, request

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
dbname = "/home/pi/templog.db"
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

app = Flask(__name__)

@app.route('/temp')
def index():
    return render_template("index.html", temp=read_temp())


@app.route('/temp/temp')
def current_temp():
    return str(read_temp())

@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    if request.method == 'POST':
        os.system("sudo shutdown now")
        return render_template("shutdown.html", shutting_down=True)
    else:
        return render_template("shutdown.html", shutting_down=False)
