from PIL import Image, ImageDraw, ImageFont
from generate.constants_generate import *
from generate.draw_square import draw_square
from generate.add_centered_text import add_centered_text
from generate.generate_2 import generate_2
from generate.generate_3 import generate_3

if __name__ == "__main__":
    dict_comp = ["фыркъа", "гæды", "куыдз", "къуда уыры", "хæфс", "тигр", "бæлон", "маймули", "халон", "сæгъ", "арс",
                 "бирæгъ", "рувас", "тæрхъус", "тыртына", "тæхсæл", "пыл", "мыст"]
    # draw_square(DIR + "square.png")
    generate_2(IMAGE_WIDTH, IMAGE_HEIGHT, DIRECTORY_IMAGES, "square.png", DIRECTORY_FINAL_FIELD, dict_comp,
               format=FORMAT_IMAGE)  # результат в final_field
    generate_3(IMAGE_WIDTH, IMAGE_HEIGHT, DIRECTORY_IMAGES, "square.png", "final_field2", dict_comp,
               format=FORMAT_IMAGE)
