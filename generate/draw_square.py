from PIL import Image, ImageDraw, ImageFont
from generate.constants_generate import *


def draw_square(final_file, wid=SQUARE_WIDTH):
    img = Image.new('RGB', (wid, wid), 'white')
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, wid - 1, wid - 1], outline='black', width=2)

    draw.line([0, 0, wid - 1, wid - 1], fill='black', width=2)
    draw.line([wid - 1, 0, 0, wid - 1], fill='black', width=2)

    img.save(final_file)