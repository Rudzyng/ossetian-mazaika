from PIL import Image, ImageFont
from generate.constants_generate import *
from generate.add_centered_text import add_centered_text


def safe_paste(background, overlay, coords):
    """Безопасная вставка с учётом прозрачности"""
    if overlay.mode == 'RGBA':
        background.paste(overlay, coords, overlay.split()[3])
    else:
        background.paste(overlay, coords)


def generate_3(img_width, img_height, image_direct, path_sq, final_direct, comp, format="png"):
    rotations = [-90, 0, 90, 0]
    coords_for_image = [(0, img_height), (img_width, 0), (2 * img_width, img_height), (img_width, img_height * 2)]
    indexes_images = [(0, 2), (1, 3), (0, 1), (1, 3), (0, 2), (1, 2), (0, 2, 3), (1, 2), (1,)]
    indexes_text = [(1, 3), (0, 2), (2, 3), (0, 2), (1, 3), (0, 3), (1,), (0, 3), (0, 2, 3)]
    pairs = [[(2, 2), (1, 0)], [(7, 3), (4, 1)], [(1, 2), (8, 3)], [(0, 3), (6, 1)]]
    pairs += [[(3, 2), (5, 0)], [(2, 3), (3, 0)], [(8, 2), (7, 0), (0, 1)], [(4, 3), (8, 0)], [(5, 3)]]
    field_text = [["", "", "", ""] for _ in range(9)]

    count_text = 0
    font = ImageFont.truetype("generate/fonts/candara.ttf", 56)
    for i in range(9):
        for j in range(len(pairs[i])):
            x, y = pairs[i][j]
            field_text[x][y] = comp[count_text]
            count_text += 1

    counter_img = 1
    for i in range(9):
        background = Image.open(f"generate/{path_sq}")

        if len(indexes_images[i]) == 2:
            overlay1 = Image.open(f"generate/{image_direct}/{counter_img}{format}")
            rotated1 = overlay1.rotate(rotations[indexes_images[i][0]], expand=True)
            safe_paste(background, rotated1, coords_for_image[indexes_images[i][0]])
            counter_img += 1

            overlay2 = Image.open(f"generate/{image_direct}/{counter_img}{format}")
            rotated2 = overlay2.rotate(rotations[indexes_images[i][1]], expand=True)
            safe_paste(background, rotated2, coords_for_image[indexes_images[i][1]])
            counter_img += 1

            y_coord = 100
            text1 = field_text[i][indexes_text[i][0]]
            background = background.rotate(rotations[indexes_text[i][0]], expand=True)
            if indexes_text[i][0] == 3:
                y_coord = 500
            add_centered_text(background, text1, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][0]], expand=True)

            text2 = field_text[i][indexes_text[i][1]]
            background = background.rotate(rotations[indexes_text[i][1]], expand=True)
            if indexes_text[i][1] == 3:
                y_coord = 500
            add_centered_text(background, text2, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][1]], expand=True)

        elif len(indexes_images[i]) == 1:
            overlay1 = Image.open(f"generate/{image_direct}/{counter_img}{format}")
            rotated1 = overlay1.rotate(rotations[indexes_images[i][0]], expand=True)
            safe_paste(background, rotated1, coords_for_image[indexes_images[i][0]])
            counter_img += 1

            y_coord = 100
            text1 = field_text[i][indexes_text[i][0]]
            background = background.rotate(rotations[indexes_text[i][0]], expand=True)
            if indexes_text[i][0] == 3:
                y_coord = 500
            add_centered_text(background, text1, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][0]], expand=True)

            text2 = field_text[i][indexes_text[i][1]]
            background = background.rotate(rotations[indexes_text[i][1]], expand=True)
            if indexes_text[i][1] == 3:
                y_coord = 500
            add_centered_text(background, text2, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][1]], expand=True)

            text3 = field_text[i][indexes_text[i][2]]
            background = background.rotate(rotations[indexes_text[i][2]], expand=True)
            if indexes_text[i][2] == 3:
                y_coord = 500
            add_centered_text(background, text3, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][2]], expand=True)
        else:
            overlay1 = Image.open(f"generate/{image_direct}/{counter_img}{format}")
            rotated1 = overlay1.rotate(rotations[indexes_images[i][0]], expand=True)
            safe_paste(background, rotated1, coords_for_image[indexes_images[i][0]])
            counter_img += 1

            overlay2 = Image.open(f"generate/{image_direct}/{counter_img}{format}")
            rotated2 = overlay2.rotate(rotations[indexes_images[i][1]], expand=True)
            safe_paste(background, rotated2, coords_for_image[indexes_images[i][1]])
            counter_img += 1

            overlay3 = Image.open(f"generate/{image_direct}/{counter_img}{format}")
            rotated3 = overlay3.rotate(rotations[indexes_images[i][2]], expand=True)
            safe_paste(background, rotated3, coords_for_image[indexes_images[i][2]])
            counter_img += 1

            y_coord = 100
            text1 = field_text[i][indexes_text[i][0]]
            background = background.rotate(rotations[indexes_text[i][0]], expand=True)
            if indexes_text[i][0] == 3:
                y_coord = 500
            add_centered_text(background, text1, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][0]], expand=True)

        background.save(f"generate/{final_direct}/{i + 1}{format}")
