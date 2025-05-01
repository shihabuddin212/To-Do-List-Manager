import os
from PIL import Image, ImageDraw, ImageFont

# Create a 256x256 white image
img = Image.new('RGBA', (256, 256), color=(255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Draw a blue-green rounded rectangle (task list)
draw.rounded_rectangle([(40, 50), (216, 206)], radius=15, fill=(60, 180, 210, 255))

# Draw task lines (white)
line_positions = [90, 130, 170]
for y in line_positions:
    draw.line([(60, y), (196, y)], fill=(255, 255, 255), width=4)

# Draw checkmarks on first two tasks
checkmark_positions = [(70, 80), (70, 120)]
for x, y in checkmark_positions:
    draw.line([(x, y), (x + 10, y + 10)], fill=(255, 255, 255), width=4)
    draw.line([(x + 10, y + 10), (x + 20, y - 5)], fill=(255, 255, 255), width=4)

# Save as icon
img.save('todo_icon.ico')

print("Icon created successfully: todo_icon.ico") 