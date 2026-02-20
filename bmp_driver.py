from bmp280_i2c import BMP280I2C

def bmp_init(i2c):
    return BMP280I2C(0x76, i2c)

def bmp_read(bmp280):
    return bmp280.measurements

if __name__ == '__main__':

    i2c0 = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
    print(i2c0.scan()) 
    i2c = BMP280I2C(0x76, i2c0)  # address may be different

    while True:
        readout = i2c.measurements
        print(f"Temperature: {readout['t']} °C, pressure: {readout['p']} hPa, altitude: {readout['a']} m.")
        sleep(1)
