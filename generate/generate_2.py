from PIL import Image, ImageFont
from .add_centered_text import add_centered_text
import os


def generate_2(img_width, img_height, images_dir, square_path, output_dir, words, format="png"):
    rotations = [-90, 0, 90, 0]
    coords_for_image = [(0, img_height), (img_width, 0), (2 * img_width, img_height), (img_width, img_height * 2)]
    indexes_images = [(0, 2), (1, 3), (1, 3), (0, 2)]
    indexes_text = [(1, 3), (0, 2), (0, 2), (1, 3)]
    pairs = [[(1, 2), (1, 0)], [(3, 3), (3, 1)], [(0, 3), (0, 1)], [(2, 2), (2, 0)]]
    field_text = [["", "", "", ""] for _ in range(4)]

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
    for i in range(4):
        for j in range(2):
            x, y = pairs[i][j]
            field_text[x][y] = words[count_text]
            count_text += 1

    counter_img = 1
    for i in range(4):
        # Открываем фон (конвертируем в RGB)
        background = Image.open(square_path).convert('RGB')

        # Первая картинка - конвертируем в RGB
        overlay1_path = os.path.join(images_dir, f"{counter_img}.png")
        if not os.path.exists(overlay1_path):
            for ext in ['.jpg', '.jpeg']:
                test_path = os.path.join(images_dir, f"{counter_img}{ext}")
                if os.path.exists(test_path):
                    overlay1_path = test_path
                    break
        overlay1 = Image.open(overlay1_path).convert('RGB')
        rotated1 = overlay1.rotate(rotations[indexes_images[i][0]])
        background.paste(rotated1, coords_for_image[indexes_images[i][0]])
        counter_img += 1

        # Вторая картинка - конвертируем в RGB
        overlay2_path = os.path.join(images_dir, f"{counter_img}.png")
        if not os.path.exists(overlay2_path):
            for ext in ['.jpg', '.jpeg']:
                test_path = os.path.join(images_dir, f"{counter_img}{ext}")
                if os.path.exists(test_path):
                    overlay2_path = test_path
                    break
        overlay2 = Image.open(overlay2_path).convert('RGB')
        rotated2 = overlay2.rotate(rotations[indexes_images[i][1]])
        background.paste(rotated2, coords_for_image[indexes_images[i][1]])
        counter_img += 1

        y_coord = 100
        text1 = field_text[i][indexes_text[i][0]]
        background = background.rotate(rotations[indexes_text[i][0]])
        add_centered_text(background, text1, background.width // 2, y_coord, font)
        background = background.rotate(-rotations[indexes_text[i][0]])

        text2 = field_text[i][indexes_text[i][1]]
        background = background.rotate(rotations[indexes_text[i][1]])
        if indexes_text[i][1] == 3:
            y_coord = 500
        add_centered_text(background, text2, background.width // 2, y_coord, font)
        background = background.rotate(-rotations[indexes_text[i][1]])

        output_path = os.path.join(output_dir, f"{i + 1}{format}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        background.save(output_path)
        print(f"Сохранено: {output_path}")