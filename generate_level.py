import PIL

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

field = [["" for i in range(WIDTH_FIELD)] for x in range(HEIGHT_FIELD)]
indexes_images = [[0, 2], [1, 3], [0, 2], [1, 3]]