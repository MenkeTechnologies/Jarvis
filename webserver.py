#!/usr/bin/env python3
# {{{ MARK:Header
# **************************************************************
##### Author: MenkeTechnologies
##### GitHub: https://github.com/MenkeTechnologies
##### Date: Mon Nov  4 18:32:14 EST 2019
##### Purpose: python3 script to
##### Notes: env FLASK_APP=hello.py flask run
# }}}***********************************************************

import os
from flask import Flask, render_template, request
app = Flask("jarvis")
import time
prev_time = time.time()


@app.route('/')
def webprint():
    if "IP" in os.environ.items():
        ip = os.environ.get("IP")
    else:
        ip = "127.0.0.1"
    return render_template('index.html', ip=ip)

@app.route('/setcar')
def setcar():
    global prev_time
    cur_time = time.time()
    time_diff = cur_time - prev_time

    if time_diff > .4:
        prev_time = time.time()
        print(f"time diff was {time_diff}")
        xpos = float(request.args.get("x"))
        ypos = float(request.args.get("y"))
        print(f"we got {xpos} and {ypos}")
    else:
        pass
        # print(f"time diff was {time_diff}")
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
