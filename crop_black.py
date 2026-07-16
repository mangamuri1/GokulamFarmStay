import os
from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

images_dir = "images"
for filename in ["1.png", "2.png", "3.png", "4.png"]:
    filepath = os.path.join(images_dir, filename)
    if os.path.exists(filepath):
        im = Image.open(filepath)
        trimmed_im = trim(im)
        trimmed_im.save(filepath)
        print(f"Trimmed {filename}")
