
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