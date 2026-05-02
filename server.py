from flask import Flask, render_template, redirect, request, jsonify, session
from forms.RegisterForm import RegisterForm
from forms.LoginForm import LoginForm
from data.User import User
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort

from constants import APP_SECRET_KEY
from utils.get_points import get_points
from utils.post_points import post_points
from utils.login import login as API_login


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
@app.route("/index")
def index():
    user_id = session.get("user_id", None)
    user_points = session.get("user_points", None)
    error = session.get("error")

    return render_template("index.html", user_id=user_id, points=user_points, error=error)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/play_level1')
@login_required
def play_level1():
    return render_template('playlevel1.html')


@app.route('/play_level2')
@login_required
def play_level2():
    return render_template("playlevel2.html")


@app.route('/play_level3')
@login_required
def play_level3():
    return render_template("playlevel1.html")


@app.route('/create')
@login_required
def create():
    return render_template("base.html")


def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/mozaika.db")
    main()