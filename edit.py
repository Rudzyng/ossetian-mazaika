from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.Level import Level
from data.PuzzlePart import PuzzlePart
from data.User import User
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
    return render_template('editor_index.html', user=current_user)


@app.route('/create_level', methods=['GET', 'POST'])
@login_required
def create_level():
    if request.method == 'GET':
        return render_template('create_level_form.html')

    try:
        level_name = request.form.get('level_name')
        grid_size = int(request.form.get('grid_size', 2))

        if not level_name:
            flash('Название уровня обязательно', 'error')
            return redirect(url_for('create_level'))

        db_sess = db_session.create_session()

        level = Level()
        level.name = level_name
        level.grid_size = grid_size

        db_sess.add(level)
        db_sess.flush()

        total_parts = grid_size * grid_size
        for i in range(total_parts):
            part = PuzzlePart()
            part.level_id = level.id
            part.word_ossetian = request.form.get(f'word_ossetian_{i}')
            # или если несколько слов через запятую:
            # part.words = request.form.get(f'words_{i}')

            # Сохраняем картинку
            image_file = request.files.get(f'image_{i}')
            if image_file:
                filename = secure_filename(f"level_{level.id}_part_{i}_{image_file.filename}")
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                part.image_file = f"uploads/{filename}"

            db_sess.add(part)

        db_sess.commit()
        flash(f'Уровень "{level_name}" успешно создан!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        flash(f'Ошибка при создании уровня: {str(e)}', 'error')
        return redirect(url_for('create_level'))


@app.route('/edit_level/<int:level_id>', methods=['GET', 'POST'])
@login_required
def edit_level(level_id):
    db_sess = db_session.create_session()
    level = db_sess.query(Level).get(level_id)

    if not level:
        flash('Уровень не найден', 'error')
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('edit_level_form.html', level=level)

    try:
        level.name = request.form.get('level_name', level.name)

        for i, part in enumerate(level.parts):
            part.word_ossetian = request.form.get(f'word_ossetian_{i}', part.word_ossetian)

            image_file = request.files.get(f'image_{i}')
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(f"level_{level.id}_part_{i}_{image_file.filename}")
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                part.image_file = f"uploads/{filename}"

        db_sess.commit()
        flash(f'Уровень "{level.name}" успешно обновлен!', 'success')

    except Exception as e:
        flash(f'Ошибка при обновлении: {str(e)}', 'error')

    return redirect(url_for('index'))


@app.route('/delete_level/<int:level_id>')
@login_required
def delete_level(level_id):
    db_sess = db_session.create_session()
    level = db_sess.query(Level).get(level_id)

    if level:
        db_sess.delete(level)
        db_sess.commit()
        flash(f'Уровень "{level.name}" удален', 'success')
    else:
        flash('Уровень не найден', 'error')

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("editor_login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not (email and password):
        return render_template("editor_login.html", error={"message": "Заполните все поля!"})

    try:
        API_login(email, password)

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()

        if not user:
            user = User()
            user.email = email
            user.name = email.split('@')[0]
            user.surname = ""
            user.set_password(password)
            db_sess.add(user)
            db_sess.commit()

        login_user(user)

        # Сохраняем в сессию для обратной совместимости
        session["user_id"] = user.id
        session["user_email"] = user.email

        flash(f'Добро пожаловать, {user.name}!', 'success')
        return redirect(url_for("index"))

    except requests.exceptions.RequestException as e:
        print(f"Ошибка API login: {e}")
        return render_template("editor_login.html", error={"message": "Ошибка соединения с сервером"})
    except Exception as e:
        print(f"Ошибка: {e}")
        return render_template("editor_login.html", error={"message": "Неверный email или пароль"})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop("user_id", None)
    session.pop("user_email", None)
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    db_session.global_init("db/mozaika.db")
    app.run(debug=True, port=5001)