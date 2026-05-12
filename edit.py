from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager

from data import db_session
from data.Level import Level
from data.PuzzlePart import PuzzlePart
from data.User import User
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
import requests
from utils.login import login as API_login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_edit_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    levels = db_sess.query(Level).all()
    return render_template('editor_index.html', levels=levels)


@app.route('/logout')
# @login_required
def logout():
    # logout_user()
    session.pop("user_id", None)
    session.pop("user_email", None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    db_session.global_init("db/mozaika.db")
    app.run(debug=True, port=5001)