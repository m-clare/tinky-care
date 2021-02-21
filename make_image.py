import sys

from PIL import Image
from inky.inky_uc8159 import Inky

inky = Inky()

img = Image.open('./assets/origami_photo.jpg')

w, h = img.size

img = img.resize((600, 448))
img.show()
# x0 = (w_new - w_cropped) / 2
# x1 = x0 + w_cropped
# y0 = 0
# y1 = h_new

# img = img.crop((x0, y0, x1, y1))

# img.show()

pal_img = Image.new("P", (1, 1))
pal_img.putpalette((0, 0, 0,
                   255, 255, 255,
                   0, 255, 0,
                   0, 0, 255,
                   255, 0, 0,
                   255, 255, 0,
                   255, 140, 0,
                   255, 255, 255) + (0, 0, 0) * 248)

img = img.convert("RGB").quantize(palette=pal_img)
inky.set_image(img)
inky_display.show()
# img.show()

