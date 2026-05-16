from flask import Flask, render_template, jsonify, request
from data import db_session
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ossetian_mozaika_secret_key'

db_session.global_init("db/mozaika.db")


def calculate_points(time_seconds):
    thresholds = {10: 10, 20: 8, 30: 6, 40: 4, 60: 2}

    for limit, points in thresholds.items():
        if time_seconds < limit:
            return points
    return 0


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", counters=list(range(1, 3)))


@app.route('/play_level1')
def play_level1():
    return render_template('playlevel1.html')


@app.route('/play_level2')
def play_level2():
    return render_template("playlevel2.html")


@app.route('/rules')
def rules():
    return render_template("rules.html")


# @app.route('/api/save_level_result', methods=['POST'])
# def save_level_result():
#     """Сохранение результата (без привязки к пользователю)"""
#     data = request.get_json()
#     if not data:
#         return jsonify({'success': False, 'error': 'No data'}), 400
#
#     level = data.get('level')
#     time_seconds = data.get('time_seconds')
#     time_formatted = data.get('time_formatted')
#
#     if level not in [1, 2] or time_seconds is None:
#         return jsonify({'success': False, 'error': 'Invalid data'}), 400
#
#     points = calculate_points(time_seconds)
#
#     return jsonify({
#         'success': True,
#         'message': 'Результат получен',
#         'points': points,
#         'time_formatted': time_formatted
#     })


if __name__ == "__main__":
    app.run(port=5000)
