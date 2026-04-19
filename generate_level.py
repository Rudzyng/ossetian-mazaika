from PIL import Image, ImageDraw, ImageFont

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


def text_on_pic(picture, text, pos, color=(0, 0, 0), txt_font="arial.ttf", size=36):
    image = Image.open(picture)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(txt_font, size)
    draw.text(pos, text, font=font, fill=color)
    image.save('output.png')


def add_centered_text(image, text, center_x, center_y, font, color=(0, 0, 0)):
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = center_x - text_width // 2
    y = center_y - text_height // 2
    
    draw.text((x, y), text, font=font, fill=color)
    return image


def generate(img_width, img_height, image_direct, format, field_direct, final_direct, comp):
    # нумерация в блоке:
    #    1
    #  0   2
    #    3
    rotations = [-90, 0, 90, 0]
    coords_for_image = [(0, img_height), (img_width, 0), (2 * img_width, img_height), (img_width, img_height * 2)]
    indexes_images = [(0, 2), (1, 3), (1, 3), (0, 2)]
    indexes_text = [(1, 3), (0, 2), (0, 2), (1, 3)]
    pairs = []
    counter = 1
    for i in range(4):
        background = Image.open(f"{field_direct}/{i + 1}{format}")
        overlay1 = Image.open(f"{image_direct}/{counter}{format}")
        rotated1 = overlay1.rotate(rotations[indexes_images[i][0]])
        background.paste(rotated1, coords_for_image[indexes_images[i][0]], rotated1)
        counter += 1

        overlay2 = Image.open(f"{image_direct}/{counter}{format}")
        rotated2 = overlay2.rotate(rotations[indexes_images[i][1]])
        background.paste(rotated2, coords_for_image[indexes_images[i][1]], rotated2)
        counter += 1
        background.save(f'{final_direct}/{i + 1}{format}')


if __name__ == "__main__":
    dict_comp = ["баран", "кошка", "собака", "хомяк", "лягушка", "тигр", "голубь", "обезьяна"]
    generate(IMAGE_WIDTH, IMAGE_HEIGHT, DIRECTORY_IMAGES, FORMAT_IMAGE, DIRECTORY_FIELD, DIRECTORY_FINAL_FIELD, dict_comp) # результат в final_field
    # generate_field("test")
    # text_on_pic("final_field/1.png", "тигр", (200, 100))
    img = Image.open("final_field/1.png")
    font = ImageFont.truetype("static/fonts/candara.ttf", 36)
    add_centered_text(img, "тигрæ", img.width // 2, 100, font)
    img.save("output.png")