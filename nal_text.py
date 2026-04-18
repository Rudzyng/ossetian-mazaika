from PIL import Image, ImageDraw, ImageFont

# Открываем изображение
image = Image.open('result.png')

# Создаем объект для рисования
draw = ImageDraw.Draw(image)

# Загружаем шрифт (укажите путь к вашему .ttf файлу)
# Если не указывать, используется шрифт по умолчанию
font = ImageFont.truetype("arial.ttf", 36)  # размер 36

# Текст для наложения
text = "Hello, World!"

# Координаты (x, y) - верхний левый угол текста
position = (100, 200)

# Цвет текста в RGB
color = (0, 0, 0)  # белый

# Накладываем текст
draw.text(position, text, font=font, fill=color)

# Сохраняем результат
image.save('output.png')