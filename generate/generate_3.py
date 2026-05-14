from PIL import Image, ImageFont
from .add_centered_text import add_centered_text
import os


def generate_3(img_width, img_height, images_dir, square_path, output_dir, words, format="png"):
    rotations = [-90, 0, 90, 0]
    coords_for_image = [(0, img_height), (img_width, 0), (2 * img_width, img_height), (img_width, img_height * 2)]
    indexes_images = [(0, 2), (1, 3), (0, 1), (1, 3), (0, 2), (1, 2), (0, 2, 3), (1, 2), (1,)]
    indexes_text = [(1, 3), (0, 2), (2, 3), (0, 2), (1, 3), (0, 3), (1,), (0, 3), (0, 2, 3)]
    pairs = [[(2, 2), (1, 0)], [(7, 3), (4, 1)], [(1, 2), (8, 3)], [(0, 3), (6, 1)]]
    pairs += [[(3, 2), (5, 0)], [(2, 3), (3, 0)], [(8, 2), (7, 0), (0, 1)], [(4, 3), (8, 0)], [(5, 3)]]
    field_text = [["", "", "", ""] for _ in range(9)]

    count_text = 0

    # Шрифт
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "fonts", "candara.ttf")
    if not os.path.exists(font_path):
        possible_fonts = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/tahoma.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]
        for pf in possible_fonts:
            if os.path.exists(pf):
                font_path = pf
                break

    try:
        font = ImageFont.truetype(font_path, 56)
        print(f"Шрифт загружен: {font_path}")
    except:
        font = ImageFont.load_default()

    # Заполняем слова
    for i in range(9):
        for j in range(len(pairs[i])):
            x, y = pairs[i][j]
            field_text[x][y] = words[count_text]
            count_text += 1

    counter_img = 1
    for i in range(9):
        # Фон конвертируем в RGB
        background = Image.open(square_path).convert('RGB')

        if len(indexes_images[i]) == 2:
            # Две картинки
            for img_idx in range(2):
                overlay_path = os.path.join(images_dir, f"{counter_img}.png")
                if not os.path.exists(overlay_path):
                    for ext in ['.jpg', '.jpeg']:
                        test_path = os.path.join(images_dir, f"{counter_img}{ext}")
                        if os.path.exists(test_path):
                            overlay_path = test_path
                            break
                overlay = Image.open(overlay_path).convert('RGB')
                rotated = overlay.rotate(rotations[indexes_images[i][img_idx]])
                background.paste(rotated, coords_for_image[indexes_images[i][img_idx]])
                counter_img += 1

            # Два текста
            for txt_idx in range(2):
                y_coord = 100 if indexes_text[i][txt_idx] != 3 else 500
                text = field_text[i][indexes_text[i][txt_idx]]
                background = background.rotate(rotations[indexes_text[i][txt_idx]])
                add_centered_text(background, text, background.width // 2, y_coord, font)
                background = background.rotate(-rotations[indexes_text[i][txt_idx]])

        elif len(indexes_images[i]) == 1:
            # Одна картинка
            overlay_path = os.path.join(images_dir, f"{counter_img}.png")
            if not os.path.exists(overlay_path):
                for ext in ['.jpg', '.jpeg']:
                    test_path = os.path.join(images_dir, f"{counter_img}{ext}")
                    if os.path.exists(test_path):
                        overlay_path = test_path
                        break
            overlay = Image.open(overlay_path).convert('RGB')
            rotated = overlay.rotate(rotations[indexes_images[i][0]])
            background.paste(rotated, coords_for_image[indexes_images[i][0]])
            counter_img += 1

            # Три текста
            for txt_idx in range(3):
                y_coord = 100 if indexes_text[i][txt_idx] != 3 else 500
                text = field_text[i][indexes_text[i][txt_idx]]
                background = background.rotate(rotations[indexes_text[i][txt_idx]])
                add_centered_text(background, text, background.width // 2, y_coord, font)
                background = background.rotate(-rotations[indexes_text[i][txt_idx]])

        else:
            # Три картинки
            for img_idx in range(3):
                overlay_path = os.path.join(images_dir, f"{counter_img}.png")
                if not os.path.exists(overlay_path):
                    for ext in ['.jpg', '.jpeg']:
                        test_path = os.path.join(images_dir, f"{counter_img}{ext}")
                        if os.path.exists(test_path):
                            overlay_path = test_path
                            break
                overlay = Image.open(overlay_path).convert('RGB')
                rotated = overlay.rotate(rotations[indexes_images[i][img_idx]])
                background.paste(rotated, coords_for_image[indexes_images[i][img_idx]])
                counter_img += 1

            # Один текст
            y_coord = 100 if indexes_text[i][0] != 3 else 500
            text = field_text[i][indexes_text[i][0]]
            background = background.rotate(rotations[indexes_text[i][0]])
            add_centered_text(background, text, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][0]])

        # Сохраняем результат
        output_path = os.path.join(output_dir, f"{i + 1}{format}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        background.save(output_path)
        print(f"Сохранено: {output_path}")