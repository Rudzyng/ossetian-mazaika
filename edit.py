import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests
from werkzeug.utils import secure_filename

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'yandexlyceum_edit_secret_key'
    app.config['UPLOAD_FOLDER'] = 'static/uploads/'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    from data import db_session

    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'mozaika.db')
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    db_session.global_init(db_file)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('static/images/custom_levels', exist_ok=True)

    from data.User import User

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.get(User, user_id)

    @app.route('/')
    def index():
        db_sess = db_session.create_session()
        from data.Level import Level
        if current_user.is_authenticated:
            levels = db_sess.query(Level).filter(Level.user_id == current_user.id).all()
        else:
            levels = []
        return render_template('editor_index.html', levels=levels, user=current_user)

    @app.route('/create_level', methods=['GET', 'POST'])
    def create_level():
        if request.method == 'GET':
            return render_template('create_level_form.html')

        try:
            level_name = request.form.get('level_name')
            grid_size = int(request.form.get('grid_size', 2))

            if not level_name:
                flash('Название уровня обязательно', 'error')
                return redirect(url_for('create_level'))

            total_parts = grid_size * grid_size
            total_pairs = total_parts * 2

            words = []
            images = []

            for i in range(total_pairs):
                word = request.form.get(f'word_{i}')
                image = request.files.get(f'image_{i}')

                if word:
                    words.append(word)
                if image:
                    images.append(image)

            if len(words) < total_pairs or len(images) < total_pairs:
                flash(f'Нужно загрузить {total_pairs} картинок и {total_pairs} слов', 'error')
                return redirect(url_for('create_level'))

            from data import db_session
            from data.Level import Level
            from data.PuzzlePart import PuzzlePart
            from generate.constants_generate import IMAGE_WIDTH, IMAGE_HEIGHT, FORMAT_IMAGE
            import shutil
            from PIL import Image as PILImage

            db_sess = db_session.create_session()

            level = Level()
            level.name = level_name
            level.grid_size = grid_size
            level.user_id = current_user.id
            db_sess.add(level)
            db_sess.flush()

            level_folder_name = f"level_{level.id}"

            # ПАПКА ДЛЯ КАРТИНОК ПОЛЬЗОВАТЕЛЯ
            temp_images_dir = os.path.join('generate', 'temp_images')
            os.makedirs(temp_images_dir, exist_ok=True)

            # Очищаем временную папку
            for f in os.listdir(temp_images_dir):
                f_path = os.path.join(temp_images_dir, f)
                if os.path.isfile(f_path):
                    os.remove(f_path)

            # Сохраняем картинки пользователя в PNG
            for idx, image in enumerate(images):
                img = PILImage.open(image)
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = PILImage.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img
                filename = f"{idx + 1}.png"
                filepath = os.path.join(temp_images_dir, filename)
                img.save(filepath, 'PNG')
                print(f"Сохранено: {filepath}")

            print(f"Файлы для генерации: {os.listdir(temp_images_dir)}")

            # СОЗДАЁМ SQUARE.PNG ЕСЛИ НЕТ
            square_path = os.path.join('generate', 'square.png')
            if not os.path.exists(square_path):
                from generate.draw_square import draw_square
                draw_square(square_path)
                print("square.png создан")

            # ПАПКА ДЛЯ РЕЗУЛЬТАТА (внутри generate)
            result_dir = os.path.join('generate', f'custom_level_{level.id}')
            os.makedirs(result_dir, exist_ok=True)

            # ВЫЗЫВАЕМ ГЕНЕРАЦИЮ
            if grid_size == 2:
                from generate.generate_2 import generate_2
                generate_2(
                    IMAGE_WIDTH, IMAGE_HEIGHT,
                    temp_images_dir,
                    square_path,
                    result_dir,
                    words,
                    FORMAT_IMAGE
                )

                # КОПИРУЕМ СГЕНЕРИРОВАННЫЕ ФАЙЛЫ В STATIC
                final_static_dir = os.path.join('static', 'images', 'custom_levels', level_folder_name)
                os.makedirs(final_static_dir, exist_ok=True)

                for i in range(4):
                    src = os.path.join(result_dir, f"{i + 1}{FORMAT_IMAGE}")
                    dst = os.path.join(final_static_dir, f"{i + 1}{FORMAT_IMAGE}")
                    if os.path.exists(src):
                        shutil.copy(src, dst)
                        print(f"Скопировано в static: {dst}")

                    part = PuzzlePart()
                    part.level_id = level.id
                    part.image_file = f"images/custom_levels/{level_folder_name}/{i + 1}{FORMAT_IMAGE}"
                    part.word_ossetian = words[i] if i < len(words) else ""
                    part.part_number = i
                    db_sess.add(part)

            elif grid_size == 3:
                from generate.generate_3 import generate_3
                generate_3(
                    IMAGE_WIDTH, IMAGE_HEIGHT,
                    temp_images_dir,
                    square_path,
                    result_dir,
                    words,
                    FORMAT_IMAGE
                )

                final_static_dir = os.path.join('static', 'images', 'custom_levels', level_folder_name)
                os.makedirs(final_static_dir, exist_ok=True)

                for i in range(9):
                    src = os.path.join(result_dir, f"{i + 1}{FORMAT_IMAGE}")
                    dst = os.path.join(final_static_dir, f"{i + 1}{FORMAT_IMAGE}")
                    if os.path.exists(src):
                        shutil.copy(src, dst)
                        print(f"Скопировано в static: {dst}")

                    part = PuzzlePart()
                    part.level_id = level.id
                    part.image_file = f"images/custom_levels/{level_folder_name}/{i + 1}{FORMAT_IMAGE}"
                    part.word_ossetian = words[i] if i < len(words) else ""
                    part.part_number = i
                    db_sess.add(part)

            db_sess.commit()

            # ОЧИЩАЕМ ВРЕМЕННУЮ ПАПКУ
            shutil.rmtree(temp_images_dir, ignore_errors=True)
            # УДАЛЯЕМ ВРЕМЕННУЮ ПАПКУ РЕЗУЛЬТАТА (или оставляем для отладки)
            # shutil.rmtree(result_dir, ignore_errors=True)

            flash(f'Уровень "{level_name}" успешно создан!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            print(f"Ошибка: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Ошибка при создании уровня: {str(e)}', 'error')
            return redirect(url_for('create_level'))

    @app.route('/delete_level/<int:level_id>')
    def delete_level(level_id):
        from data import db_session
        from data.Level import Level
        import shutil

        db_sess = db_session.create_session()
        level = db_sess.query(Level).filter(
            Level.id == level_id,
            Level.user_id == current_user.id
        ).first()

        if not level:
            flash('Уровень не найден или доступ запрещён', 'error')
            return redirect(url_for('index'))

        try:
            level_folder = os.path.join('static', 'images', 'custom_levels', f'level_{level.id}')
            if os.path.exists(level_folder):
                shutil.rmtree(level_folder)
                print(f"Удалена папка: {level_folder}")

            db_sess.delete(level)
            db_sess.commit()

            flash(f'Уровень "{level.name}" и все его файлы удалены', 'success')

        except Exception as e:
            print(f"Ошибка при удалении: {e}")
            flash(f'Ошибка при удалении уровня: {str(e)}', 'error')

        return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        from data import db_session
        from data.User import User
        from utils.login import login as API_login

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
                user.set_password(password)
                db_sess.add(user)
                db_sess.commit()

            login_user(user)
            session["user_id"] = user.id
            session["user_email"] = user.email

            flash('Вход выполнен успешно!', 'success')
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

    @app.route('/play_custom_level/<int:level_id>')
    def play_custom_level(level_id):
        from data import db_session
        from data.Level import Level

        db_sess = db_session.create_session()
        level = db_sess.query(Level).get(level_id)

        if not level:
            flash('Уровень не найден', 'error')
            return redirect(url_for('index'))

        parts = []
        for part in sorted(level.parts, key=lambda p: p.part_number):
            parts.append({
                'num': part.part_number + 1,
                'image': f"/static/{part.image_file}",
                'word': part.word_ossetian
            })

        return render_template('play_custom_level.html',
                               level=level,
                               parts=parts,
                               grid_size=level.grid_size)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)