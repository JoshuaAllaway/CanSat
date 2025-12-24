
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
        

def gamma_correct(r: int, g: int, b: int) -> tuple[int]:
    '''
    Decrase the gamma of an RGB565 colour to saturate it
    '''
    M = max(r << 1, g, b << 1) #find the greatest channel (r & b have a lower bit depth)
    
    gamma = 0.88 #new gamma-value
    
    #applies the gamma curve, c**gamma, to the greatest channel
    r = round(31*pow(r/31,gamma)) if r << 1 == M else r
    g = round(63*pow(g/63,gamma)) if g == M else g
    b = round(31*pow(b/31,gamma)) if b << 1 == M else b
    
    return r, g, b

def to_RGB332(buffer: bytearray) -> bytearray:
    '''
    Downscales an RGB565 bytearray to a gamma-corrected RGB332 bytearray
    '''
    out = bytearray() #RGB332 bytearray to be filled
    
    for i in range(0, len(buffer), 2): #iteartes over every byte pair
        
        value = (buffer[i] << 8) | buffer[i+1] #concatenates bytes to the full RGB565 value
        
        #masks the red, green and blue channels from the value
        r = (value >> 11) & 0x1F
        g = (value >> 5) & 0x3F
        b = value & 0x1F
        
        r, g, b = gamma_correct(r, g, b) #gamma-corrects the RGB565 value
        
        #downsacles the channels to RGB332
        r = (r >> 2) & 0x7
        g = (g >> 3) & 0x7
        b = (b >> 3) & 0x3
        
        colour = (r << 5) | (g << 2) | b #concatenates channels to the RGB332 colour
        out.append(colour)
    
    return out

def to_RGB565(buffer: bytearray) -> bytearray:
    '''
    Upscale the RGB332 bytearray to RGB565
    '''
    out = bytearray() #RGB565 bytearray to be filled
    
    for value in buffer: #iterates over every byte
        
        #masks off the red, green and blue channels
        r = (value >> 5) & 0x7
        g = (value >> 2) & 0x7
        b = value & 0x3
        
        colour = (r << 13) | (g << 8) | (b << 3) #concatenates channels to the RGB565 value
        
        #splits the colour into two bytes
        high = (colour >> 8) & 0xFF
        low = colour & 0xFF
        
        #consecutively appends each byte to the buffer
        out.append(high)
        out.append(low)
    
    return out
