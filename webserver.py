#!/usr/bin/env python3
# {{{ MARK:Header
# **************************************************************
##### Author: MenkeTechnologies
###### GitHub: https://github.com/MenkeTechnologies
##### Date: Mon Nov  4 18:32:14 EST 2019
##### Purpose: python3 script to
##### Notes: env FLASK_APP=hello.py flask run
# }}}***********************************************************

import os
from importlib import import_module

from flask import Flask, render_template, Response

app = Flask("jarvis")
import time

prev_time = time.time()

if os.environ.get("IP"):
    ip = os.environ.get("IP")
    print(f"IP {ip} from environ")
else:
    ip = "127.0.0.1"
    print("could not get IP from environ")

if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def webprint():
    return render_template('index.html', ip=ip)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
