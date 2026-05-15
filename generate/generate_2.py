from PIL import Image, ImageFont
from generate.constants_generate import *
from generate.add_centered_text import add_centered_text


def generate_2(img_width, img_height, image_direct, path_sq, final_direct, comp, format="png"):
    rotations = [-90, 0, 90, 0]
    coords_for_image = [(0, img_height), (img_width, 0), (2 * img_width, img_height), (img_width, img_height * 2)]
    indexes_images = [(0, 2), (1, 3), (1, 3), (0, 2)]
    indexes_text = [(1, 3), (0, 2), (0, 2), (1, 3)]
    pairs = [[(1, 2), (1, 0)], [(3, 3), (3, 1)], [(0, 3), (0, 1)], [(2, 2), (2, 0)]]
    field_text = [["", "", "", ""] for _ in range(4)]

    count_text = 0
    font = ImageFont.truetype("generate/fonts/candara.ttf", 56)
    for i in range(4):
        for j in range(2):
            x, y = pairs[i][j]
            field_text[x][y] = comp[count_text]
            count_text += 1

    counter_img = 1
    for i in range(4):
        background = Image.open(f"generate/{path_sq}")

        overlay1 = Image.open(f"generate/{image_direct}/{counter_img}{format}")
        rotated1 = overlay1.rotate(rotations[indexes_images[i][0]], expand=True)
        if rotated1.mode == 'RGBA':
            background.paste(rotated1, coords_for_image[indexes_images[i][0]], rotated1.split()[3])
        else:
            background.paste(rotated1, coords_for_image[indexes_images[i][0]])
        counter_img += 1

        overlay2 = Image.open(f"generate/{image_direct}/{counter_img}{format}")
        rotated2 = overlay2.rotate(rotations[indexes_images[i][1]], expand=True)
        if rotated2.mode == 'RGBA':
            background.paste(rotated2, coords_for_image[indexes_images[i][1]], rotated2.split()[3])
        else:
            background.paste(rotated2, coords_for_image[indexes_images[i][1]])
        counter_img += 1

        y_coord = 100
        text1 = field_text[i][indexes_text[i][0]]
        background = background.rotate(rotations[indexes_text[i][0]], expand=True)
        add_centered_text(background, text1, background.width // 2, y_coord, font)
        background = background.rotate(-rotations[indexes_text[i][0]], expand=True)

        text2 = field_text[i][indexes_text[i][1]]
        background = background.rotate(rotations[indexes_text[i][1]], expand=True)
        if indexes_text[i][1] == 3:
            y_coord = 500
        add_centered_text(background, text2, background.width // 2, y_coord, font)
        background = background.rotate(-rotations[indexes_text[i][1]], expand=True)

        background.save(f"generate/{final_direct}/{i + 1}{format}")
