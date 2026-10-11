from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from data import db_session
from data.User import User
from data.Level import Level
from data.PuzzlePart import PuzzlePart
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests

from constants import APP_SECRET_KEY
from utils import api

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db_session.global_init("db/mozaika.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, int(user_id))


def calculate_points(time_seconds):
    thresholds = {10: 10, 20: 8, 30: 6, 40: 4, 60: 2}
    for limit, points in thresholds.items():
        if time_seconds < limit:
            return points
    return 0


@app.route("/")
@app.route("/index")
@app.route("/start")
def index():
    # Портал открывает игру как /start?session=<id>&token=<hmac>.
    api.get_game_session_id()
    db_sess = db_session.create_session()
    levels = db_sess.query(Level).all()
    return render_template("index.html", levels=levels, counters=list(range(1, 3)))


@app.route('/rules')
def rules():
    return render_template("rules.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not (email and password):
        return render_template("login.html", error={"message": "Заполните все поля"})

    try:
        api.login(email, password)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()

        if not user:
            user = User()
            user.email = email
            user.set_password(password)
            db_sess.add(user)
            db_sess.commit()

        login_user(user)
        session["user_id"] = user.id
        session["user_email"] = user.email

        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for("index"))

    except requests.exceptions.RequestException as e:
        print(f"Ошибка API login: {e}")
        return render_template("login.html", error={"message": "Ошибка соединения с сервером"})
    except Exception as e:
        print(f"Ошибка: {e}")
        return render_template("login.html", error={"message": "Неверный email или пароль"})


@app.route('/play_custom_level/<int:level_id>')
def play_custom_level(level_id):
    db_sess = db_session.create_session()
    level = db_sess.query(Level).get(level_id)

    if not level:
        flash('Уровень не найден', 'error')
        return redirect(url_for('index'))

    parts = []
    for part in sorted(level.parts, key=lambda p: p.part_number):
        parts.append({
            'num': part.part_number + 1,
            'image': f"/static/{part.image_file}"
        })

    return render_template('play_custom_level.html',
                           level=level,
                           parts=parts,
                           grid_size=level.grid_size)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop("user_id", None)
    session.pop("user_email", None)
    return redirect(url_for("index"))


@app.route('/api/save_level_result', methods=['POST'])
def save_level_result():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data'}), 400

    level_id = data.get('level_id')
    level_num = data.get('level')
    time_seconds = data.get('time_seconds')
    time_formatted = data.get('time_formatted')

    points = calculate_points(time_seconds)
    is_new_record = False
    portal_total_points = None
    portal_error = None

    # Начисление не зависит от локального логина: пользователь уже подтверждён
    # одноразовой игровой сессией, выданной порталом iframe.
    if points > 0 and session.get("game_session_id"):
        try:
            portal_total_points = api.add_points(points)
        except api.ApiError as exc:
            portal_error = str(exc)
            app.logger.warning("Не удалось начислить баллы портала: %s", exc)

    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.get(User, current_user.id)

        if user:
            if level_id:
                score_field = f'level_{level_id}'
                pass
            elif level_num in [1, 2]:
                score_field = 'level1' if level_num == 1 else 'level2'
                current_best = getattr(user, score_field)

                if current_best is None or time_seconds < current_best:
                    setattr(user, score_field, time_seconds)
                    db_sess.commit()
                    is_new_record = True

            return jsonify({
                'success': True,
                'message': 'Новый рекорд!' if is_new_record else 'Результат сохранён',
                'points': points,
                'is_new_record': is_new_record,
                'time_formatted': time_formatted,
                'requires_login': False,
                'portal_total_points': portal_total_points,
                'portal_error': portal_error
            })

    return jsonify({
        'success': True,
        'message': 'Войдите, чтобы сохранить результат',
        'points': points,
        'is_new_record': False,
        'time_formatted': time_formatted,
        'requires_login': True,
        'portal_total_points': portal_total_points,
        'portal_error': portal_error
    })


if __name__ == "__main__":
    app.run(port=5000)
