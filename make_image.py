import sys

from PIL import Image
from inky.inky_uc8159 import Inky

inky = Inky()

img = Image.open('./assets/nova.jpg')
w, h = img.size
print(w, h)

img = img.resize((448, 600))

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

MID_PALETTE = tuple(sum(x)// 2 for x in zip(DESATURATED_PALETTE, SATURATED_PALETTE))

pal_img.putpalette(MID_PALETTE)

img = img.convert("RGB").quantize(palette=pal_img)
inky.set_image(img)
inky.show()


