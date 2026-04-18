from PIL import Image, ImageDraw, ImageFont

image = Image.open('result.png')

draw = ImageDraw.Draw(image)

font = ImageFont.truetype("arial.ttf", 36)

text = "Hello, World!"

position = (100, 200)

color = (0, 0, 0)

draw.text(position, text, font=font, fill=color)

image.save('output.png')