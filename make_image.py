import sys

from PIL import Image
from inky.inky_uc8159 import Inky

inky = Inky()

img = Image.open('./assets/nova.jpg')

w, h = img.size

img = img.resize((448, 600))

img.rotate(90)
# x0 = (w_new - w_cropped) / 2
# x1 = x0 + w_cropped
# y0 = 0
# y1 = h_new

# img = img.crop((x0, y0, x1, y1))

# img.show()

pal_img = Image.new("P", (1, 1))

DESATURATED_PALETTE = (0, 0, 0,
                       255, 255, 255,
                       0, 255, 0,
                       0, 0, 255,
                       255, 0, 0,
                       255, 255, 0,
                       255, 140, 0,
                       255, 255, 255) + (0, 0, 0) * 248

SATURATED_PALETTE = (57, 48, 57,
                     255, 255, 255,
                     58, 91, 70,
                     61, 59, 94,
                     156, 72, 75,
                     208, 190, 71,
                     177, 106, 73,
                     255, 255, 255) + (0, 0, 0) * 248

pal_img.putpalette(DESATURATED_PALETTE)

img = img.convert("RGB").quantize(palette=pal_img)
inky.set_image(img)
inky.show()


