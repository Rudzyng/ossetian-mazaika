from PIL import Image, ImageDraw

IMAGE_HEIGHT = 200
IMAGE_WIDTH = 200
WIDTH_FIELD = 2
HEIGHT_FIELD = 2
NUMBER_IMAGES = 8
DIRECTORY_IMAGES = "images_generate"
FORMAT_IMAGE = ".png"
SQUARE_WIDTH = IMAGE_HEIGHT * 3

# нумерация в блоке:
#    1
#  0   2
#    3
field = [[("", 1) for i in range(4)] for x in range(4)]
indexes_images = [[0, 2], [1, 3], [0, 2], [1, 3]]
indexes_text = [[1, 3], [0, 2], [1, 3], [0, 2]]

counter = 1
for i in range(len(indexes_images)):
    for ind_img in indexes_images[i]:
        field[i][ind_img] = (f"{DIRECTORY_IMAGES}/{counter}{FORMAT_IMAGE}", 1)
        counter += 1



def generate_square():
    img = Image.new('RGB', (SQUARE_WIDTH, SQUARE_WIDTH), 'white')
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, SQUARE_WIDTH - 1, SQUARE_WIDTH - 1], outline='black', width=2)

    draw.line([0, 0, SQUARE_WIDTH - 1, SQUARE_WIDTH - 1], fill='black', width=2)
    draw.line([SQUARE_WIDTH - 1, 0, 0, SQUARE_WIDTH - 1], fill='black', width=2)

    img.save('square.png')


