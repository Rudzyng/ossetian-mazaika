from flask import Flask, render_template, redirect, request, jsonify, session
from forms.RegisterForm import RegisterForm
from forms.LoginForm import LoginForm
from data.User import User
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
import uuid
import json
import os
from pathlib import Path


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def get_default_slots():
    static_folder = Path('static/images')
    
    if not static_folder.exists():
        print(f"❌ Папка не найдена: {static_folder.absolute()}")
        print(f"Текущая директория: {os.getcwd()}")
    
    # Вариант 1: Если файлы точно есть в static/images/
    slots = {
        'slot1': {
            'id': 'img1',
            'url': '/static/images/image1.png',  # Убедитесь, что файл существует
            'title': 'Моя картинка 1'
        },
        'slot2': {
            'id': 'img2',
            'url': '/static/images/image2.png',
            'title': 'Моя картинка 2'
        },
        'slot3': {
            'id': 'img3',
            'url': '/static/images/image3.png',
            'title': 'Моя картинка 3'
        },
        'slot4': {
            'id': 'img4',
            'url': '/static/images/image4.png',
            'title': 'Моя картинка 4'
        }
    }
    
    # Проверяем каждый файл
    for slot, data in slots.items():
        file_path = data['url'].replace('/static/', 'static/')
        if os.path.exists(file_path):
            print(f"✅ {slot}: {file_path} - найден")
        else:
            print(f"❌ {slot}: {file_path} - НЕ НАЙДЕН!")
            print(f"   Ищем в: {os.path.abspath(file_path)}")
    
    return slots


@app.route('/update_positions', methods=['POST'])
def update_positions():
    """Обновляет порядок картинок"""
    data = request.json
    new_order = data.get('order', {})
    
    # Сохраняем новый порядок в сессии
    session['slots'] = new_order
    session.modified = True
    
    return jsonify({'status': 'success', 'message': 'Позиции обновлены'})

@app.route('/reset', methods=['POST'])
def reset():
    """Сбрасывает порядок к начальному"""
    session['slots'] = get_default_slots()
    session.modified = True
    return jsonify({'status': 'success', 'message': 'Сброшено'})


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", counters=list(range(1, 4)))


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
    if 'slots' not in session:
        session['slots'] = get_default_slots()
    return render_template('playlevel.html', slots=session['slots'])


@app.route('/play_level2')
@login_required
def play_level2():
    return render_template("base.html")


@app.route('/play_level3')
@login_required
def play_level3():
    return render_template("base.html")


@app.route('/create')
@login_required
def create():
    return render_template("base.html")


def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/mozaika.db")
    main()