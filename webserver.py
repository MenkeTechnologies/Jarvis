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

from flask import Flask, render_template, url_for, flash, Response, redirect, request
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import LoginForm

app = Flask("jarvis")

app.config['SECRET_KEY'] = '27e361b60bbfd4d1a3560a5a6a0385df'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jarvis.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
@app.route('/driver')
@login_required
def driver():
    return render_template('driver.html', ip=ip)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('driver'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('driver'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
