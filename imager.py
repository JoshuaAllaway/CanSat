
X, Y = 48,36
depth = 3
gamma = 0.88

def resize(buffer, w, h, factor):
    new_w = w//factor
    new_h = h//factor
    print(new_h,new_w)
    out = bytearray(new_h*new_w*2)
    i_out = 0
    for y_out in range(new_h):
        y = y_out*factor
        
        for x_out in range(new_w):
            x = x_out*factor
            
            i_in = (y*w + x)*2
            out[i_out] = buffer[i_in]
            out[i_out+1] = buffer[i_in+1]
            i_out += 2
    return out

def flatten(data):
    flattened = []
    for x in data:
        for y in x:
            for z in y:
                flattened.append(z)
    return flattened

def setGamma(rgb):
    global gamma
    M = max(rgb)
    new_rgb = [255*(c/255)**gamma if c == M else c for c in rgb]
    return new_rgb

def RGBquantise(rgb):
    global depth, gamma
    rgb = setGamma(rgb)
    s = (2**depth-1)/255
    rgb = [round(c*s) for c in rgb]
    return rgb

def toRGB(buffer):
    
    out = []
    for i in range(0, len(buf), 2):
        value = (buffer[i] << 8) | buffer[i+1]
        r = (value >> 11) & 0x1F
        g = (value >> 5) & 0x3F
        b = value & 0x1F
        out.append(RGBquantise(r << 3, g << 2, b << 3))
    
    return out

def pack(img):
    bitstring = 0
    for rgb in img:
        for channel in rgb:
            bitstring <<= depth
            bitstring |= channel
    
    return bitstring.to_bytes()

def unpack(data):
    bitstring = 0
    pixels = []
    rgb = ()
    for byte in data:
        bitstring <<= 8
        bitstring |= byte
        
    for _ in range(X*Y*3):
        channel = bitstring & 2**depth - 1
        bitstring >>= depth
        rgb.append(channel)
        if len(rgb) == 3:
            pixels.append(rgb)
    return pixels


if __name__ == '__main__':
    packed = pack(img_in)
    print(packed,packed.len/8000)

    img_out = unpack(packed)
    print(img_in == img_out)

