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

app = Flask("jarvis")

@app.route('/')
def webprint():
    return render_template('index.html')

@app.route('/setcar')
def setcar():
    x = request.args.get("x")
    y = request.args.get("y")
    print(f"we got {x} and {y}")
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
