from PIL import Image, ImageDraw, ImageFont, ImageOps
from time import sleep
import serial

def fit_image(txt, width, height):
    w,h = width*3,height*3
    s = height*2
    attempts = 0
    direction = 0
    while attempts < 100:
        print s
        attempts += 1
        first_row = h
        last_row = 0
        first_col = w
        last_col = 0
        im = Image.new('RGB', (w,h), color='white')
        d = ImageDraw.Draw(im)
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
        d.text((width,height), text, font=font, fill=(0,0,0))
        pixels = list(im.convert(mode='1').getdata())
        pixels = [pixels[i * w:(i + 1) * w] for i in xrange(h)]
        for i in range(w):
            for j in range(h):
                if pixels[j][i] == 0:
                    first_col = min(first_col, i)
                    first_row = min(first_row, j)
                    last_col = max(last_col, i)
                    last_row = max(last_row, j)
        if (last_col - first_col + 1 > width) or (last_row - first_row + 1 > height):
            s -= 1
        else:
            im.crop((first_col-1, first_row-1, last_col+2, last_row+2))
            return im

# Base image
text = "coil winder".upper()

im = fit_image(text, 300, 24)

im.save('label.png')

im = ImageOps.flip(im)
# Convert into a list of lists of numbers, where 0 is black and 255 is white.
im = im.convert(mode='1')
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

up_position = '105\n'
down_position = '90\n'
start_motor = '182\n'
stop_motor = '0\n'


# Send the pixel data as up and down commands.
ser = serial.Serial('/dev/ttyACM0')
sleep(1)
print ser.write(down_position)
sleep(1)
print ser.write(up_position)
sleep(1)
print ser.write(start_motor)
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
ser.write(stop_motor)
print '0'
