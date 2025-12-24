
def resize(buffer: bytearray, w: int, h: int, factor: int) -> bytearray:
    '''
    Downscale an RGB565 bytearray by the specified factor
    '''
    #calculates the size of the downsacled bytearray
    new_w = w//factor
    new_h = h//factor
    out = bytearray(new_h*new_w*2) #2 bytes per pixel
    
    i_out = 0
    for y_out in range(new_h): #for each row
        y = y_out*factor #calculates the input row
        
        for x_out in range(new_w): #for each column
            x = x_out*factor #calculates the input column
            
            i_in = (y*w + x)*2 #finds the current pixel index
            
            #allocates the pixel bytes
            out[i_out] = buffer[i_in]
            out[i_out+1] = buffer[i_in+1]
            
            i_out += 2 #increments the index
    
    return out