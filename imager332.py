
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

def to_RGB332(buffer):
    
    out = bytearray()
    for i in range(0, len(buffer), 2):
        value = (buffer[i] << 8) | buffer[i+1]
        r = (value >> 13) & 0x7
        g = (value >> 8) & 0x7
        b = (value >> 3) & 0x3
        colour = (r << 5) | (g << 2) | b
        out.append(colour)
    
    return out

def to_RGB565(buffer):
    
    out = bytearray()
    for value in buffer:
        r = (value >> 5) & 0x7
        g = (value >> 2) & 0x7
        b = value & 0x3
        colour = (r << 13) | (g << 8) | (b << 3)
        high = (colour >> 8) & 0xFF
        low = colour & 0xFF
        out.append(high)
        out.append(low)
    
    return out
