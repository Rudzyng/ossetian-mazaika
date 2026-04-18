from PIL import Image, ImageDraw, ImageFont

def add_centered_text(image, text, center_x, center_y, font, color=(0, 0, 0)):
    draw = ImageDraw.Draw(image)
    
    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Вычисляем позицию для центрирования
    x = center_x - text_width // 2
    y = center_y - text_height // 2
    
    draw.text((x, y), text, font=font, fill=color)
    return image

# Использование
img = Image.open('result.png')
font = ImageFont.truetype("arial.ttf", 36)
add_centered_text(img, "тигр", img.width//2, 100, font)
img.save('output.png')