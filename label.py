from PIL import Image, ImageDraw, ImageFont, ImageOps
from time import sleep
import serial

# Base image
im = Image.new('RGB', (300,20), color='white')

# Place the text
d = ImageDraw.Draw(im)
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 30)
d.text((50,-5), "Hello World", font=font, fill=(0,0,0))

# Since the labels are printed bottom line first, flip it.
im = ImageOps.flip(im)
# Save it as a png for reference
im.save('label.png')

# Convert into a list of lists of numbers, where 0 is black and 255 is white.
im = im.convert(mode='1')
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

# Send the pixel data as up and down commands.
ser = serial.Serial('/dev/ttyACM0')
for line in pixels:
    # Wait for the trigger time
    trigger = ser.readline()
    print 'trig'
    prev_pixel = 0
    # Send an up or down servo command each time the current pixel is a
    # different color to the previous one.
    for pixel in line:
        if pixel > 0 and prev_pixel == 0:
            ser.write('100\n')
            print '100\n'
        elif pixel == 0 and prev_pixel > 0:
            ser.write('90\n')
            print '90\n'
        prev_pixel = pixel
        # This determines the spacing of the pixels. at 0.05, it runs over an:
        # the picture gets skewed.
        sleep(0.04)
