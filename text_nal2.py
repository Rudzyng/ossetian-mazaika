from PIL import Image, ImageDraw, ImageFont

def add_centered_text(image, text, center_x, center_y, font, color=(0, 0, 0), rotation=0):
    """
    Накладывает центрированный текст на изображение
    
    Параметры:
    - rotation: 0 (горизонтально), 90 (вертикально сверху вниз), -90 (вертикально снизу вверх)
    """
    
    # Проверяем корректность параметра rotation
    if rotation not in [0, 90, -90]:
        raise ValueError("rotation должен быть 0, 90 или -90")
    
    # Конвертируем в RGBA для работы с прозрачностью
    if image.mode != 'RGBA':
        original_mode = image.mode
        image = image.convert('RGBA')
    else:
        original_mode = 'RGBA'
    
    # Получаем размеры текста
    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if rotation == 0:
        # Горизонтальный текст
        text_img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((0, 0), text, font=font, fill=color)
        
        x = center_x - text_width // 2
        y = center_y - text_height // 2
        
    else:
        # Вертикальный текст
        # Меняем ширину и высоту местами для вертикального текста
        text_img = Image.new('RGBA', (text_height, text_width), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((0, 0), text, font=font, fill=color)
        
        if rotation == 90:
            text_img = text_img.rotate(90, expand=True, resample=Image.BICUBIC)
        else:  # rotation == -90
            text_img = text_img.rotate(-90, expand=True, resample=Image.BICUBIC)
        
        x = center_x - text_img.width // 2
        y = center_y - text_img.height // 2
    
    # Накладываем текст
    image.paste(text_img, (x, y), text_img)
    
    # Возвращаем в исходный режим
    if original_mode != 'RGBA':
        image = image.convert(original_mode)
    
    return image

# Использование
img = Image.open('result.png')
font = ImageFont.truetype("arial.ttf", 36)

# Разные варианты
add_centered_text(img, "горизонтально", img.width//2, 80, font, rotation=0)
add_centered_text(img, "вертикально", img.width//2, 180, font, color=(255, 0, 0), rotation=90)
add_centered_text(img, "вверх ногами", img.width//2, 280, font, color=(0, 0, 255), rotation=-90)

img.save('output.png')