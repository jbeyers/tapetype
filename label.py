from PIL import Image, ImageDraw, ImageFont, ImageOps
from time import sleep
import serial

im = Image.new('RGB', (300,20), color='white')
d = ImageDraw.Draw(im)

#font = ImageFont.truetype('ubuntu.ttf', 18)
#font = ImageFont.load_default()
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 30)
d.text((50,-5), "Hello World", font=font, fill=(0,0,0))
im = ImageOps.flip(im)
im.save('label.png')

im = im.convert(mode='1')
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
print pixels

# The image is now flipped, converted and ready for processing

ser = serial.Serial('/dev/ttyACM0')
for line in pixels:
    # Wait for the trigger time
    trigger = ser.readline()
    print 'trig'
    prev_pixel = 0
    for pixel in line:
        if pixel > 0 and prev_pixel == 0:
            ser.write('100\n')
            print '100\n'
        elif pixel == 0 and prev_pixel > 0:
            ser.write('90\n')
            print '90\n'
        prev_pixel = pixel
        sleep(0.04)


