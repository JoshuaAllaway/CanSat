from time import sleep
from sx127x import *
from machine import SPI, Pin

def radio_init(spi, freq):
    
    lora = SX127x(spi=spi,
              pins={'ss' : Pin(17, Pin.OUT),
                    'reset':Pin(14, Pin.OUT),
                    'dio_0':Pin(15, Pin.IN)},
              parameters = {
            'frequency': freq, 
            'tx_power_level': 2, 
            'signal_bandwidth': 125E3,    
            'spreading_factor': 8, 
            'coding_rate': 5, 
            'preamble_length': 8,
            'implicit_header': False, 
            'sync_word': 0x12, 
            'enable_CRC': False,
            'invert_IQ': False,
            })
    
    return lora

def receive(lora):

    for _ in range(100):
        if lora.received_packet():
            print('something here')
            payload = lora.read_payload()
            print(payload)

def send(lora, msg):
    
    counter = 0
    print("LoRa Sender")

    while counter <= 2:
        payload = msg.format(counter)
        print("Sending packet: \n{}\n".format(payload))
        lora.println(payload)

        counter += 1
        sleep(.25)


if __name__ == '__main__':
    
    spi = SPI(0, baudrate=5000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))

    freq = 433E6
    
    lora = SX127x(spi=spi,
              pins={'ss' : Pin(17, Pin.OUT),
                    'reset':Pin(14, Pin.OUT),
                    'dio_0':Pin(15, Pin.IN)},
              parameters = {
            'frequency': freq, 
            'tx_power_level': 2, 
            'signal_bandwidth': 125E3,    
            'spreading_factor': 8, 
            'coding_rate': 5, 
            'preamble_length': 8,
            'implicit_header': False, 
            'sync_word': 0x12, 
            'enable_CRC': False,
            'invert_IQ': False,
            })
    while True:
        send(lora, 'Hello')
        receive(lora)
