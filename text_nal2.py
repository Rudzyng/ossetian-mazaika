from PIL import Image, ImageDraw, ImageFont

def add_centered_text(image, text, center_x, center_y, font, color=(0, 0, 0), angle=0):
    draw = ImageDraw.Draw(image)
    
    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if angle == 0:
        # Без поворота - используем простой метод
        x = center_x - text_width // 2
        y = center_y - text_height // 2
        draw.text((x, y), text, font=font, fill=color)
    else:
        # С поворотом - создаем отдельный слой
        # Создаем изображение для текста с небольшим запасом
        padding = 20
        text_img = Image.new('RGBA', (text_width + padding, text_height + padding), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        
        # Рисуем текст
        text_draw.text((padding//2, padding//2), text, font=font, fill=color)
        
        # Поворачиваем
        text_img = text_img.rotate(angle, expand=True, resample=Image.BICUBIC)
        
        # Вычисляем позицию для вставки
        x = center_x - text_img.width // 2
        y = center_y - text_img.height // 2
        
        # Вставляем с учетом прозрачности
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        image.paste(text_img, (x, y), text_img)
    
    return image

# Пример использования с разными углами
img = Image.open('result.png')
font = ImageFont.truetype("arial.ttf", 36)

# Разные варианты поворота
add_centered_text(img, "тигр", img.width//2, 80, font, angle=0)           # 0 градусов
add_centered_text(img, "тигр", img.width//2, 160, font, angle=30)         # 30 градусов
add_centered_text(img, "тигр", img.width//2, 240, font, angle=-45)        # -45 градусов
add_centered_text(img, "тигр", img.width//2, 320, font, angle=90)         # 90 градусов
add_centered_text(img, "тигр", img.width//2, 400, font, angle=180)        # 180 градусов

img.save('output.png')