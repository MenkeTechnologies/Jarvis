#!/usr/bin/env python3
# {{{ MARK:Header
# **************************************************************
##### Author: MenkeTechnologies
##### GitHub: https://github.com/MenkeTechnologies
##### Date: Mon Nov  4 18:32:14 EST 2019
##### Purpose: python3 script to
##### Notes: env FLASK_APP=hello.py flask run
# }}}***********************************************************

from flask import Flask, render_template, request
import sys
import smbus
channel = 1
address = 0xa
bus = smbus.SMBus(1)
app = Flask("jarvis")
import time
prev_time = time.time()


@app.route('/')
def webprint():
    return render_template('index.html')

@app.route('/setcar')
def setcar():
    cur_time = time.time()
    time_diff = cur_time - prev_time

    if time_diff > 40:
        xpos = float(request.args.get("x"))
        ypos = float(request.args.get("y"))
        ESCset = 45*ypos+90
        turnSet =90*xpos+90
        data = [int(turnSet),int(ESCset)]
        bus.write_i2c_block_data(address, 1,data)
        print(f"we got {xpos} and {ypos}")
    else:
        print(f"time diff was {time_diff}")
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
