from PIL import Image
from numpy import array
import imager332 as imager

img = Image.open('Assets\Map 5.jpg').convert('RGB')
img.show()

w,h = img.size

def to_rgb565(img: Image.Image) -> bytearray:
    """
    Convert a PIL RGB image to a 1D RGB565 bytearray.
    """

    width, height = img.size
    pixels = img.load()

    out = bytearray(width * height * 2)
    i = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Convert 8-bit channels to RGB565
            r5 = (r >> 3) & 0x1F
            g6 = (g >> 2) & 0x3F
            b5 = (b >> 3) & 0x1F

            value = (r5 << 11) | (g6 << 5) | b5

            out[i]   = (value >> 8) & 0xFF  # high byte
            out[i+1] = value & 0xFF         # low byte
            i += 2

    return out

def to_rgb(buf: bytearray, width: int, height: int):
    """
    Convert a 1D RGB565 bytearray into a list of (R,G,B) tuples.
    """
    out = []
    for i in range(0, len(buf), 2):
        value = (buf[i] << 8) | buf[i+1]

        # Extract 5/6/5 bits
        r5 = (value >> 11) & 0x1F
        g6 = (value >> 5) & 0x3F
        b5 = value & 0x1F

        # Scale back to 8-bit
        r = r5 << 3
        g = g6 << 2
        b = b5 << 3

        out.append((r, g, b))

    return out

def to_image(buf: bytearray, width: int, height: int) -> Image.Image:
    """
    Convert RGB565 bytearray to a PIL RGB image.
    """
    rgb = to_rgb(buf, width, height)
    img = Image.new("RGB", (width, height))
    img.putdata(rgb)
    return img

buffer = to_rgb565(img)
print(len(buffer)/1000)

factor = h//38

buffer = imager.resize(buffer, w, h, factor)
bits = imager.to_RGB332(buffer)
print(f'{len(bits)/1000}')
bits = imager.to_RGB565(bits)
img = to_image(bits, w//factor, h//factor)
img.show()