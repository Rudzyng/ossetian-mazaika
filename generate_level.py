from PIL import Image, ImageDraw

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


def generate(img_width, img_height, image_direct, format, field_direct, final_direct):
    # нумерация в блоке:
    #    1
    #  0   2
    #    3
    coords_for_image = [(0, img_height), (img_width, 0), (2 * img_width, img_height), (img_width, img_height * 2)]
    field = [[("", 1) for i in range(4)] for x in range(4)]
    indexes_images = [(0, 2), (1, 3), (0, 2), (1, 3)]
    indexes_text = [(1, 3), (0, 2), (1, 3), (0, 2)]
    counter = 1
    for i in range(4):
        background = Image.open(f'{field_direct}/{i + 1}.png')
        overlay1 = Image.open(f"{image_direct}/{counter}{format}")
        if overlay1.mode == 'RGBA':
            background.paste(overlay1, coords_for_image[indexes_images[i][0]], overlay1)
        else:
            background.paste(overlay1, coords_for_image[indexes_images[i][0]])
        counter += 1
        overlay2 = Image.open(f"{image_direct}/{counter}{format}")
        if overlay2.mode == 'RGBA':
            background.paste(overlay2, coords_for_image[indexes_images[i][1]], overlay2)
        else:
            background.paste(overlay2, coords_for_image[indexes_images[i][1]])
        counter += 1
        background.save(f'{final_direct}/{i + 1}{format}')


if __name__ == "__main__":
    generate(IMAGE_WIDTH, IMAGE_HEIGHT, DIRECTORY_IMAGES, FORMAT_IMAGE, DIRECTORY_FIELD, DIRECTORY_FINAL_FIELD) # результат в final_field
    generate_field("test")