from PIL import Image, ImageDraw, ImageFont, ImageOps
from time import sleep
import serial

# Base image
im = Image.new('RGB', (300,20), color='white')
text = "breadboard".upper()
font_size = 22
offset = -5
up_position = '105\n'
down_position = '90\n'
max_height = 24
max_width = 300

# Place the text
d = ImageDraw.Draw(im)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
d.text((20, offset), text, font=font, fill=(0,0,0))

# Save it as a png for reference
im.save('label.png')

# Since the labels are printed bottom line first, flip it.
im = ImageOps.flip(im)

# Convert into a list of lists of numbers, where 0 is black and 255 is white.
im = im.convert(mode='1')
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

# Send the pixel data as up and down commands.
ser = serial.Serial('/dev/ttyACM0')
ser.write('181')
for line in pixels:
    # Wait for the trigger time
    trigger = ser.readline()
    print 'trig'
    prev_pixel = 0
    # Send an up or down servo command each time the current pixel is a
    # different color to the previous one.
    for pixel in line:
        if pixel > 0 and prev_pixel == 0:
            ser.write(up_position)
            print up_position
        elif pixel == 0 and prev_pixel > 0:
            ser.write(down_position)
            print down_position
        prev_pixel = pixel
        # This time delay determines the spacing of the pixels.
        sleep(0.06)
ser.write('0')
