from PIL import Image, ImageDraw, ImageFont


def add_centered_text(image, text, center_x, center_y, font, color=(0, 0, 0)):
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = center_x - text_width // 2
    y = center_y - text_height // 2

    draw.text((x, y), text, font=font, fill=color)
    return image
