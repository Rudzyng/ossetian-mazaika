from PIL import Image, ImageDraw
from typing import Tuple, Optional

IMAGE_HEIGHT = 200
IMAGE_WIDTH = 200
WIDTH_FIELD = 2
HEIGHT_FIELD = 2
NUMBER_IMAGES = 8
DIRECTORY_IMAGES = "images_generate"
FORMAT_IMAGE = ".png"
SQUARE_WIDTH = IMAGE_HEIGHT * 3
DIRECTORY_FINAL_FIELD = "final_field"
DIRECTORY_FIELD = "field"

def generate_square():
    img = Image.new('RGB', (SQUARE_WIDTH, SQUARE_WIDTH), 'white')
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, SQUARE_WIDTH - 1, SQUARE_WIDTH - 1], outline='black', width=2)

    draw.line([0, 0, SQUARE_WIDTH - 1, SQUARE_WIDTH - 1], fill='black', width=2)
    draw.line([SQUARE_WIDTH - 1, 0, 0, SQUARE_WIDTH - 1], fill='black', width=2)

    img.save('square.png')


def place_image(background_path, overlay_path, output_path, position, size=None, alpha=True):
    """
        background_path: путь к фоновому изображению
        overlay_path: путь к вставляемому изображению
        output_path: путь для сохранения результата
        position: координаты (x, y) для вставки
        size: новый размер для вставляемого изображения (опционально)
        alpha: учитывать ли альфа-канал
    """
    background = Image.open(background_path)
    overlay = Image.open(overlay_path)

    if size:
        overlay = overlay.resize(size)

    if alpha and overlay.mode == 'RGBA':
        background.paste(overlay, position, overlay)
    else:
        background.paste(overlay, position)
    
    background.save(output_path)


# place_image('field/1.png', 'images_generate/1.png', 'result.png', (IMAGE_WIDTH, IMAGE_HEIGHT * 2))


def generate(img_width, img_height, image_direct, format, field_direct, final_direct):
    # нумерация в блоке:
    #    1
    #  0   2
    #    3
    coords_for_image = [(0, img_height), (img_width, 0), (2 * img_width, img_height), (img_width, img_height * 2)]
    # place_image('field/1.png', 'images_generate/2.png', 'result.png', coords_for_image[3])
    field = [[("", 1) for i in range(4)] for x in range(4)]
    indexes_images = [(0, 2), (1, 3), (0, 2), (1, 3)]
    indexes_text = [(1, 3), (0, 2), (1, 3), (0, 2)]
    counter = 1
    for i in range(len(indexes_images)):
        for ind_img in indexes_images[i]:
            field[i][ind_img] = (f"{image_direct}/{counter}{format}", 1)
            counter += 1
            place_image(f'{field_direct}/{i + 1}.png', field[i][ind_img][0], f'{final_direct}/{i + 1}.png', coords_for_image[ind_img])

generate(IMAGE_WIDTH, IMAGE_HEIGHT, DIRECTORY_IMAGES, FORMAT_IMAGE, DIRECTORY_FIELD, DIRECTORY_FINAL_FIELD)