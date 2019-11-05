#!/usr/bin/env python3
# {{{ MARK:Header
# **************************************************************
##### Author: MenkeTechnologies
##### GitHub: https://github.com/MenkeTechnologies
##### Date: Mon Nov  4 18:32:14 EST 2019
##### Purpose: python3 script to
##### Notes: env FLASK_APP=hello.py flask run
# }}}***********************************************************

from flask import Flask, render_template

app = Flask("jarvis")

@app.route('/')
def webprint():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
