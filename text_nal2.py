from PIL import Image, ImageDraw, ImageFont

def add_centered_text(image, text, center_x, center_y, font, color=(0, 0, 0), angle=0):
    # Получаем размеры текста без поворота
    temp_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Создаем временное изображение для текста
    text_image = Image.new('RGBA', (text_width + 20, text_height + 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_image)
    
    # Рисуем текст на временном изображении
    draw.text((10, 10), text, font=font, fill=color)
    
    # Поворачиваем изображение с текстом
    if angle != 0:
        text_image = text_image.rotate(angle, expand=True, resample=Image.BICUBIC)
    
    # Вычисляем позицию для вставки (с учетом поворота)
    x = center_x - text_image.width // 2
    y = center_y - text_image.height // 2
    
    # Вставляем текст на основное изображение
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    image.paste(text_image, (x, y), text_image)
    
    return image

# Использование
img = Image.open('result.png')
font = ImageFont.truetype("arial.ttf", 36)

# Текст без поворота
add_centered_text(img, "тигр", img.width//2, 100, font, angle=0)

# Текст с поворотом на 45 градусов
add_centered_text(img, "тигр", img.width//2, 200, font, color=(255,0,0), angle=45)

# Текст с поворотом на -30 градусов
add_centered_text(img, "тигр", img.width//2, 300, font, color=(0,255,0), angle=-30)

img.save('output.png')