from flask import Flask, render_template, request, redirect, url_for, flash
from data import db_session
from data.Level import Level
from data.PuzzlePart import PuzzlePart
import os
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_edit_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    db_sess = db_session.create_session()
    levels = db_sess.query(Level).all()
    return render_template('editor_index.html', levels=levels)


@app.route('/create_level', methods=['GET', 'POST'])
def create_level():
    if request.method == 'GET':
        return render_template('create_level_form.html')

    if request.method == 'POST':
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

            db_sess = db_session.create_session()

            level = Level()
            level.name = level_name
            level.grid_size = grid_size
            db_sess.add(level)
            db_sess.flush()

            from generate.constants_generate import IMAGE_WIDTH, IMAGE_HEIGHT, FORMAT_IMAGE, DIR, DIRECTORY_IMAGES

            temp_images_dir = os.path.join(DIR, DIRECTORY_IMAGES)
            os.makedirs(temp_images_dir, exist_ok=True)

            for idx, image in enumerate(images):
                ext = os.path.splitext(image.filename)[1]
                filename = f"{idx + 1}{ext if ext else '.png'}"
                filepath = os.path.join(temp_images_dir, filename)
                image.save(filepath)

            level_folder_name = f"level_{level.id}"
            final_dir = os.path.join('static', 'custom_levels', level_folder_name)
            os.makedirs(final_dir, exist_ok=True)

            if grid_size == 2:
                from generate.generate_2 import generate_2
                generate_2(
                    IMAGE_WIDTH, IMAGE_HEIGHT,
                    DIRECTORY_IMAGES,
                    "square.png",
                    f"../static/custom_levels/{level_folder_name}",
                    words,
                    FORMAT_IMAGE
                )

                for i in range(4):
                    part = PuzzlePart()
                    part.level_id = level.id
                    part.image_file = f"custom_levels/{level_folder_name}/{i + 1}{FORMAT_IMAGE}"
                    part.word_ossetian = words[i] if i < len(words) else ""
                    part.part_number = i
                    db_sess.add(part)

            elif grid_size == 3:
                from generate.generate_3 import generate_3
                generate_3(
                    IMAGE_WIDTH, IMAGE_HEIGHT,
                    DIRECTORY_IMAGES,
                    "square.png",
                    f"../static/custom_levels/{level_folder_name}",
                    words,
                    FORMAT_IMAGE
                )

                for i in range(9):
                    part = PuzzlePart()
                    part.level_id = level.id
                    part.image_file = f"custom_levels/{level_folder_name}/{i + 1}{FORMAT_IMAGE}"
                    part.word_ossetian = words[i] if i < len(words) else ""
                    part.part_number = i
                    db_sess.add(part)

            db_sess.commit()

            shutil.rmtree(temp_images_dir, ignore_errors=True)

            flash(f'Уровень "{level_name}" успешно создан!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            print(f"Ошибка: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Ошибка при создании уровня: {str(e)}', 'error')
            return redirect(url_for('create_level'))

    return render_template('create_level_form.html')


@app.route('/delete_level/<int:level_id>')
def delete_level(level_id):
    db_sess = db_session.create_session()
    level = db_sess.query(Level).get(level_id)

    if level:
        level_folder_name = f"level_{level.id}"
        final_dir = os.path.join('static', 'custom_levels', level_folder_name)
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)

        db_sess.delete(level)
        db_sess.commit()
        flash(f'Уровень "{level.name}" удален', 'success')
    else:
        flash('Уровень не найден', 'error')

    return redirect(url_for('index'))


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
            'image': f"/static/{part.image_file}",
            'word': part.word_ossetian
        })

    return render_template('play_custom_level.html',
                           level=level,
                           parts=parts,
                           grid_size=level.grid_size)


if __name__ == '__main__':
    db_session.global_init("db/mozaika.db")
    app.run(port=5001)
