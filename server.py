import os
import sys
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from constants import APP_SECRET_KEY
from utils.get_points import get_points
from utils.post_points import post_points
from utils.login import login as API_login


def calculate_points(time_seconds):
    """
    Правила:
    < 10 сек - 10 баллов
    < 20 сек - 8 баллов
    < 30 сек - 6 баллов
    < 40 сек - 4 балла
    < 60 сек - 2 балла
    >= 60 сек - 0 баллов
    """
    if time_seconds < 10:
        return 10
    elif time_seconds < 20:
        return 8
    elif time_seconds < 30:
        return 6
    elif time_seconds < 40:
        return 4
    elif time_seconds < 60:
        return 2
    else:
        return 0


def create_app():
    """
    Фабрика для создания экземпляра веб-приложения.
    Инициализирует все компоненты игры.
    """
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

    from data import db_session

    # Инициализируем базу данных
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'mozaika.db')
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    db_session.global_init(db_file)

    # Инициализируем Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from data.User import User

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.get(User, user_id)

    # 5. Регистрируем маршруты
    @app.route("/")
    @app.route("/index")
    def index():
        user_id = session.get("user_id", None)
        user_points = session.get("user_points", None)
        error = session.get("error")

        return render_template("index.html",
                               user_id=user_id,
                               points=user_points,
                               error=error,
                               counters=list(range(1, 3)))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "GET":
            return render_template("login.html")

        email = request.form.get("email")
        password = request.form.get("password")

        if not (email and password):
            return render_template("login.html", error={"message": "Заполните все поля"})

        try:
            API_login(email, password)
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == email).first()

            if not user:
                user = User(email=email)
                user.set_password(password)
                db_sess.add(user)
                db_sess.commit()

            login_user(user)

            return redirect(url_for("index"))

        except requests.exceptions.RequestException as e:
            print(f"Ошибка API login: {e}")
            return render_template("login.html", error={"message": "Ошибка соединения с сервером"})
        except ValueError:
            return render_template("login.html", error={"message": "Неверный ответ от сервера"})

    @app.route('/logout')
    def logout():
        session.pop("user_id", None)
        session.pop("user_points", None)
        return render_template("index.html")

    @app.route('/play_level1')
    def play_level1():
        user_id = session.get("user_id", None)
        return render_template('playlevel1.html', user_id=user_id)

    @app.route('/play_level2')
    def play_level2():
        user_id = session.get("user_id", None)
        return render_template("playlevel2.html", user_id=user_id)

    @app.route('/rules')
    def rules():
        return render_template("base.html")

    @app.route("/points", methods=["GET", "POST"])
    def points():
        if request.method == "GET":
            session["user_points"] = get_points()
        elif request.method == "POST":
            try:
                points = int(request.form.get("points", 0))
                session["user_points"] = post_points(points)
            except Exception as e:
                session["error"] = e

        return redirect(url_for("index"))

    @app.route('/api/save_level_result', methods=['POST'])
    def save_level_result():
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data'}), 400

        level = data.get('level')
        time_seconds = data.get('time_seconds')
        time_formatted = data.get('time_formatted')

        if level not in [1, 2] or time_seconds is None:
            return jsonify({'success': False, 'error': 'Invalid data'}), 400

        points = calculate_points(time_seconds)

        if current_user.is_authenticated:
            db_sess = db_session.create_session()
            user = db_sess.get(User, current_user.id)

            if user:
                score_field = 'level1' if level == 1 else 'level2'
                current_best = getattr(user, score_field)

                if current_best is None or points > current_best:
                    setattr(user, score_field, points)
                    db_sess.commit()
                    is_new_record = True
                else:
                    is_new_record = False
                return jsonify({
                    'success': True,
                    'message': 'Новый рекорд!' if is_new_record else 'Результат сохранён',
                    'points': points,
                    'is_new_record': is_new_record,
                    'saved_to_db': True
                })

        if 'level_results' not in session:
            session['level_results'] = {}

        session['level_results'][f'level_{level}'] = {
            'points': points,
            'time_formatted': time_formatted,
            'timestamp': datetime.utcnow().isoformat()
        }
        session.modified = True

        return jsonify({
            'success': True,
            'message': 'Результат сохранён временно (войдите для постоянного сохранения)',
            'points': points,
            'saved_to_db': False,
            'requires_login': True
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)