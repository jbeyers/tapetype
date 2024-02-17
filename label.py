"""
Take the list of text labels and rework them to fit onto the 300x24 canvas,
and output them as arrays for the Arduino code to use to print the labels.
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps

MAX_WIDTH = 204
MAX_HEIGHT = 24

labels = [
    # 'RING BELL',
    # 'PARTS VADA',
    # 'E-SATA',
    # 'HDD SCAV',
    'PI ZERO',
    # 'GLASSES',
    # 'DC FANS',
    # 'T-SLOT',
    # '3D PRINTER',
    'HDD MRMR',
    'RC PROPS',
    # 'DRILLING',
    # 'HINGES, HANDLES',
    # 'CATCHES, LOCKS',
    # 'COMPUTER CABLES',
    # 'ADAPTERS, GADGETS',
    # 'ODDS & ENDS',
    # 'LANYARDS',
    # 'STRAPS',
    # 'RANDOM',
    # 'OLD NAILS',
    # 'HEADPHONES',
    # 'AV CABLES',
    # 'USB',
    # 'USB',
    # 'USB',
    # 'USB ADAPTERS',
    # 'E-BIKE',
    # 'E-BIKE',
    # 'BOSCH BATTERIES',
    # 'MAGNETS',
    # 'CRATE LID',
    # 'LATCHES',
    # 'USELESS MACHINE',
    # 'SCOOBY/TUBES',
    # 'FLOOR SLIDERS',
    # 'CASTERS',
    # 'ANTISTATIC BAGS',
    # 'LDPE',
    # 'KEYS & LOCKS',
    # 'CDR/HDD PARTS',
    # 'BAGS, PADDING',
    # 'FLASHLIGHTS',
    # 'CHIPBOARD SCREWS',
    # 'TAPES',
    # 'GLUE',
    # 'WALL PLUGS, NAILS',
    # 'CABLE MOUNTS',
    # '>= M6',
    # 'NUTS & BOLTS',
    # '< M6',
    # 'HDD PARTS',
    # 'HDD PARTS',
    # 'TUBING',
    # 'INTERESTING', 
    # 'MATERIALS',
    # 'TRINKETS',
    # 'TRINKETS',
    # 'AIR PUMP',
    # 'RESISTORS',
    'LA MAKER FAIRE',
    'JOHAN.BEYERS.CO.ZA',
]

def fit_image(txt, width, height):
    w,h = width*3,height*3
    s = height*2
    attempts = 0
    while attempts < 100:
        attempts += 1
        first_row = h*3
        last_row = 0
        first_col = w*3
        last_col = 0
        im = Image.new('RGB', (w,h), color='white')
        d = ImageDraw.Draw(im)
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
        d.text((width,height), txt, font=font, fill=(0,0,0))
        pixels = list(im.convert(mode='1').getdata())
        pixels = [pixels[i * w:(i + 1) * w] for i in range(h)]
        for i in range(w):
            for j in range(h):
                if pixels[j][i] == 0:
                    first_col = min(first_col, i)
                    first_row = min(first_row, j)
                    last_col = max(last_col, i)
                    last_row = max(last_row, j)
        if (last_col - first_col > width) or (last_row - first_row > height):
            s -= 1
        else:
            return im.crop((first_col, first_row, last_col, last_row))

def get_pixels(text):
    im = fit_image(text, MAX_WIDTH, MAX_HEIGHT)
    im.save('label.png')
    im = ImageOps.flip(im)
    # Convert into a list of lists of numbers, where 0 is black and 255 is white.
    im = im.convert(mode='1', dither=Image.Dither.NONE)
    # Convert this to a list of 0 and 1 values
    pixels = [1 if i == 0 else 0 for i in im.getdata()]
    width, height = im.size
    return [pixels[i * width:(i + 1) * width] for i in range(height)]

label_pixels = []
for label in labels:
    pixels = get_pixels(label)

    # Pad the label to MAX_WIDTH, left aligned
    padding = MAX_WIDTH - len(pixels[0])
    if padding:
        for i in range(len(pixels)):
            pixels[i] = pixels[i] + [0]*padding

    # Vertically center the label
    # The pixel lines start from the bottom, so rather have it one too low.
    lines_to_add = MAX_HEIGHT - len(pixels)
    if lines_to_add:
        num,remainder = divmod(lines_to_add, 2)
        for i in range(num):
            pixels.insert(0, [0]*MAX_WIDTH)
        for i in range(num + remainder):
            pixels.append([0]*MAX_WIDTH)

    label_pixels.append(pixels)

# Convert the nested lists to text Arduino arrays and supporting constants

label_strings = []
for label in label_pixels:
    row_strings = []
    for row in label:
        row_strings.append('{' + ','.join(str(i) for i in row) + '}')
    label_strings.append('  {\n    ' + ',\n    '.join(row_strings) + '\n  }' )

final_string = f"const byte labels[{len(labels)}][{MAX_HEIGHT}][{MAX_WIDTH}] PROGMEM = {{\n" + ','.join(label_strings) + '\n};\n'

with open('label_pixels.txt', 'w') as f:
    f.write(final_string)    
    f.write(f"const int num_labels = {len(labels)};\n")
    f.write(f"const int label_height = {MAX_HEIGHT};\n")
    f.write(f"const int label_width = {MAX_WIDTH};\n")
