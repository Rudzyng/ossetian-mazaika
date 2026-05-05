from PIL import Image, ImageDraw, ImageFont
from generate.constants_generate import *


def draw_square(final_file, wid=SQUARE_WIDTH):
    img = Image.new('RGB', (wid, wid), 'white')
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, wid - 1, wid - 1], outline='black', width=2)

    draw.line([0, 0, wid - 1, wid - 1], fill='black', width=2)
    draw.line([wid - 1, 0, 0, wid - 1], fill='black', width=2)

    img.save(final_file)


def generate_field(final_dir, wid=WIDTH_FIELD, hei=HEIGHT_FIELD, wid_sqr=SQUARE_WIDTH):
    for i in range(wid * hei):
        draw_square(f"{final_dir}/{i + 1}.png", wid=wid_sqr)


def add_centered_text(image, text, center_x, center_y, font, color=(0, 0, 0)):
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = center_x - text_width // 2
    y = center_y - text_height // 2
    
    draw.text((x, y), text, font=font, fill=color)
    return image


def generate_2(img_width, img_height, image_direct, format, field_direct, final_direct, comp):
    # нумерация в блоке:
    #    1
    #  0   2
    #    3
    rotations = [-90, 0, 90, 0]
    coords_for_image = [(0, img_height), (img_width, 0), (2 * img_width, img_height), (img_width, img_height * 2)]
    indexes_images = [(0, 2), (1, 3), (1, 3), (0, 2)]
    indexes_text = [(1, 3), (0, 2), (0, 2), (1, 3)]
    pairs = [[(1, 2), (1, 0)], [(3, 3), (3, 1)], [(0, 3), (0, 1)], [(2, 2), (2, 0)]]
    field_text = [["", "", "", ""] for _ in range(4)]

    count_text = 0
    font = ImageFont.truetype(DIR + "fonts/candara.ttf", 56)
    for i in range(4):
        for j in range(2):
            x, y = pairs[i][j]
            field_text[x][y] = comp[count_text]
            count_text += 1

    counter_img = 1
    for i in range(4):
        background = Image.open(DIR + f"{field_direct}/{i + 1}{format}")
        overlay1 = Image.open(DIR + f"{image_direct}/{counter_img}{format}")
        rotated1 = overlay1.rotate(rotations[indexes_images[i][0]])
        background.paste(rotated1, coords_for_image[indexes_images[i][0]], rotated1)
        counter_img += 1

        overlay2 = Image.open(DIR + f"{image_direct}/{counter_img}{format}")
        rotated2 = overlay2.rotate(rotations[indexes_images[i][1]])
        background.paste(rotated2, coords_for_image[indexes_images[i][1]], rotated2)
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

        background.save(DIR + f'{final_direct}/{i + 1}{format}')


def generate_3(img_width, img_height, image_direct, format, field_direct, final_direct, comp):
    # нумерация в блоке:
    #    1
    #  0   2
    #    3
    rotations = [-90, 0, 90, 0]
    coords_for_image = [(0, img_height), (img_width, 0), (2 * img_width, img_height), (img_width, img_height * 2)]
    indexes_images = [(0, 2), (1, 3), (0, 1), (1, 3), (0, 2), (1, 2), (0, 2, 3), (1, 2), (1,)]
    indexes_text = [(1, 3), (0, 2), (2, 3), (0, 2), (1, 3), (0, 3), (1,), (0, 3), (0, 2, 3)]
    pairs = [[(2, 2), (1, 0)], [(7, 3), (4, 1)], [(1, 2), (8, 3)], [(0, 3), (6, 1)]]
    pairs += [[(3, 2), (5, 0)], [(2, 3), (3, 0)], [(8, 2), (7, 0), (0, 1)], [(4, 3), (8, 0)], [(5, 3)]]
    field_text = [["", "", "", ""] for _ in range(9)]

    count_text = 0
    font = ImageFont.truetype(DIR + "fonts/candara.ttf", 56)
    for i in range(9):
        for j in range(len(pairs[i])):
            x, y = pairs[i][j]
            field_text[x][y] = comp[count_text]
            count_text += 1

    counter_img = 1
    for i in range(9):
        background = Image.open(DIR + f"{field_direct}/{i + 1}{format}")
        if len(indexes_images[i]) == 2:
            overlay1 = Image.open(DIR + f"{image_direct}/{counter_img}{format}")
            rotated1 = overlay1.rotate(rotations[indexes_images[i][0]])
            background.paste(rotated1, coords_for_image[indexes_images[i][0]], rotated1)
            counter_img += 1

            overlay2 = Image.open(DIR + f"{image_direct}/{counter_img}{format}")
            rotated2 = overlay2.rotate(rotations[indexes_images[i][1]])
            background.paste(rotated2, coords_for_image[indexes_images[i][1]], rotated2)
            counter_img += 1

            y_coord = 100
            text1 = field_text[i][indexes_text[i][0]]
            background = background.rotate(rotations[indexes_text[i][0]])
            if indexes_text[i][0] == 3:
                y_coord = 500
            add_centered_text(background, text1, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][0]])

            text2 = field_text[i][indexes_text[i][1]]
            background = background.rotate(rotations[indexes_text[i][1]])
            if indexes_text[i][1] == 3:
                y_coord = 500
            add_centered_text(background, text2, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][1]])
        elif len(indexes_images[i]) == 1:
            overlay1 = Image.open(DIR + f"{image_direct}/{counter_img}{format}")
            rotated1 = overlay1.rotate(rotations[indexes_images[i][0]])
            background.paste(rotated1, coords_for_image[indexes_images[i][0]], rotated1)
            counter_img += 1

            y_coord = 100
            text1 = field_text[i][indexes_text[i][0]]
            background = background.rotate(rotations[indexes_text[i][0]])
            if indexes_text[i][0] == 3:
                y_coord = 500
            add_centered_text(background, text1, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][0]])

            text2 = field_text[i][indexes_text[i][1]]
            background = background.rotate(rotations[indexes_text[i][1]])
            if indexes_text[i][1] == 3:
                y_coord = 500
            add_centered_text(background, text2, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][1]])

            text3 = field_text[i][indexes_text[i][2]]
            background = background.rotate(rotations[indexes_text[i][2]])
            if indexes_text[i][2] == 3:
                y_coord = 500
            add_centered_text(background, text3, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][2]])
        else:
            overlay1 = Image.open(DIR + f"{image_direct}/{counter_img}{format}")
            rotated1 = overlay1.rotate(rotations[indexes_images[i][0]])
            background.paste(rotated1, coords_for_image[indexes_images[i][0]], rotated1)
            counter_img += 1

            overlay2 = Image.open(DIR + f"{image_direct}/{counter_img}{format}")
            rotated2 = overlay2.rotate(rotations[indexes_images[i][1]])
            background.paste(rotated2, coords_for_image[indexes_images[i][1]], rotated2)
            counter_img += 1

            overlay3 = Image.open(DIR + f"{image_direct}/{counter_img}{format}")
            rotated3 = overlay3.rotate(rotations[indexes_images[i][2]])
            background.paste(rotated3, coords_for_image[indexes_images[i][2]], rotated3)
            counter_img += 1

            y_coord = 100
            text1 = field_text[i][indexes_text[i][0]]
            background = background.rotate(rotations[indexes_text[i][0]])
            if indexes_text[i][0] == 3:
                y_coord = 500
            add_centered_text(background, text1, background.width // 2, y_coord, font)
            background = background.rotate(-rotations[indexes_text[i][0]])

        background.save(DIR + f'{final_direct}/{i + 1}{format}')


if __name__ == "__main__":
    dict_comp = ["фыркъа", "гæды", "куыдз", "къуда уыры", "хæфс", "тигр", "бæлон", "маймули", "халон", "сæгъ", "арс", "бирæгъ", "рувас", "тæрхъус", "тыртына", "тæхсæл", "пыл", "мыст"]
    generate_2(IMAGE_WIDTH, IMAGE_HEIGHT, DIRECTORY_IMAGES, FORMAT_IMAGE, DIRECTORY_FIELD, DIRECTORY_FINAL_FIELD, dict_comp) # результат в final_field
    # generate_field(DIR + "field1", 3, 3)
    # text_on_pic("final_field/1.png", "тигр", (200, 100))
    generate_3(IMAGE_WIDTH, IMAGE_HEIGHT, DIRECTORY_IMAGES, FORMAT_IMAGE, "field1", "final_field2", dict_comp)