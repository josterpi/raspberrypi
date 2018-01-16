
import os
 
from flask import Flask, render_template, request

from temperature import read_temp

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
