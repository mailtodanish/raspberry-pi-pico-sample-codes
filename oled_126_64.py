from machine import Pin, Timer
import utime as time
from pico_i2c_lcd import I2cLcd
from machine import I2C
from dht import DHT11, InvalidChecksum
from sh1106 import SH1106_I2C
import framebuf
import freesans20
import writer

WIDTH  = 128                                            # oled display width
HEIGHT = 64                                            # oled display height

i2c = I2C(0)                                            # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config
oled = SH1106_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display


h = [
0x00, 0x00, 0x00, 0x00, 0x07, 0xC0, 0x00, 0x00, 0x07, 0xE0, 0x00, 0x18, 0x04, 0x20, 0x00, 0x18,
0x04, 0x38, 0x00, 0x3C, 0x04, 0x20, 0x00, 0x24, 0x04, 0x30, 0x00, 0x66, 0x04, 0x30, 0x00, 0x24,
0x04, 0x20, 0x00, 0x3C, 0x05, 0xB8, 0x00, 0x00, 0x05, 0xA0, 0x06, 0x00, 0x05, 0xA0, 0x0E, 0x00,
0x05, 0xB0, 0x0B, 0x00, 0x05, 0xA0, 0x19, 0x00, 0x05, 0xB8, 0x11, 0x80, 0x05, 0xA0, 0x11, 0x80,
0x05, 0xA0, 0x1B, 0x00, 0x0D, 0xA0, 0x0E, 0x00, 0x19, 0xB8, 0x00, 0x18, 0x31, 0x8C, 0x00, 0x18,
0x21, 0x84, 0x00, 0x24, 0x67, 0xC6, 0x00, 0x66, 0x47, 0xE2, 0x00, 0x42, 0x47, 0xE2, 0x00, 0x42,
0x47, 0xE2, 0x00, 0x42, 0x47, 0xC6, 0x00, 0x7E, 0x61, 0x84, 0x00, 0x18, 0x30, 0x0C, 0x00, 0x00,
0x18, 0x18, 0x00, 0x00, 0x0F, 0xF0, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

# Raspberry Pi logo as 32x32 bytearray
buffer_water = bytearray(h)
buffer_sun = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x81\x81\x00\x00`\x06\x00\x00`\x06\x00\x00\x13\xc8\x00\x00\x0c0\x00\x00\x0c0\x00\x00\x10\x08\x00\x07\x90\t\xe0\x07\x90\t\xe0\x00\x10\x08\x00\x00\x0c0\x00\x00\x0c0\x00\x00\x13\xc8\x00\x00`\x06\x00\x00`\x06\x00\x00\x81\x81\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

mar = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x000\x00\x00\x00\x00\x00<\x00\x1f\x00\x00\x00\x00\x07\xe8\x00\xc3\x80\x00\x00\x00\x07\x80\xc0a\xe0\x00\x00\x00\x07\x8f\xf8\xf1p\x00\x00\x00\x0e\x1f@\x7f\x80\x00\x00\x008>\x00\x03\x00\x00\x00\x00x~\x02\x01\x00\x00\x00\x00pp\x02\x01\x02\x040\x00\xf0pNc'\x80\x00\x00\xa0q\xff\xc0w\xc0\x00\x01\xb8a\xff\x00\x7f\xc0\x00\x01\x19\xe0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x07\x80\x00\x00\x07\x80\x00\x00\x0f\x80\x00\x00\x02\x00\x00\x00\x00\x00@\x00\x02\x00\x00\x00\x00\x08\x00\x00D\x00\x00\x00\x03\xfc\x00\x01@\x00\x00\x00\x01\xf2\x00\x01@\x00\x00\x00\x01\xd8\x00\x10`\x0e\x00\x01\x80@\x00\x1c\xa0?\xc0?\xf0`\x00\x0c\xf0@\x01\x00\x11\xf8\x04\x0cR\x00\xc0\x10\t\xf8\x00\x0c{\xa0p<%\xf9\x00\x0c;\xe08 \x07\xf3\x00\x00-\xdf\xc8\x1f\xcf\xf1\x00\x00\x15\xfc\x08\x03\xff\xe9\x80\x00\x15\xa0\x08\x00\xe7\xf0\x80\x00\xd9\x80\x08\x00\x03\xe0\xc0\x00\xdc\x008\x00\x03\xf0\xc0\x01\xfc\x008\x00\x03\xb8p\x00\xfc\x005\x80\x03\xb80\x00|\x007\xc0\x0f\xfc0\x00\x7f\x80\x00\x00\x1f\xfc0\x00\x7f\x80\x00\x02>n\x00\x01\xff\xc0?\x82>c\xc0\x03\x1b\xe0\x7f\xe0\x1e\x03\xf0\x00\x0f\xf1\xf0\xf0\x1eC\xf0\x03\x06p\x8ep\x0f\xc1\xf0\x03\xdep\xc5\xe0\r\xc0\xf0\x01\xc7\xf0\x7f\xc0\r\xd1\xf8\x00\xff\xe0\x00\x00\r\xe0\xf83\xff\xe0\x00\x00\x0f\xe7\xf8\x13\xff\xa0\x00\x00\x0b\xff\xf8\x0c\xfaP\x00\x00\x1a?\xf0\x0c~X\x00\x006\x7f\xf0\x03\x9e^\x00\x01\xe2p\x00\x03\xfeo\x80\x1f\xc2p\x00\x01>'\xff\xff\x82x\x80\x01>3\xff\xfe\x06{\x00\x00\xbe1\xff\xe0\x04>\x00\x00\x9e9\xff\x80\x048\x00\x00\x0c\x19\xfc\x00\x04\x0c\x00\x00\x00}\xf0\x00\x04\x07\x00\x00\x00|\xf8\x00\x0e\x01\xf0\x00\x01\x9cp\x00\x08\x00\x0e\x00\x00^p\x00\x00\x00\x03\x00\x00\x0e\x00\x00\x03\x80\x00\x00\x00\x00\x00\x00\x06\x00\x00\x01\x00\x01\x00\x00\x0c\x00\x00\x00\x00\x03\x80\x00\x08\x00\x00\x00\x08\x0c\x00\x00\xb0\x00\x00")

# Load the raspberry pi logo into the framebuffer (the image is 32x32)
fb = framebuf.FrameBuffer(buffer_water, 32, 32, framebuf.MONO_HLSB)
fb1 = framebuf.FrameBuffer(buffer_sun, 32, 32, framebuf.MONO_HLSB)
fb2 = framebuf.FrameBuffer(mar, 64, 64, framebuf.MONO_HLSB)
oled.rotate(True)
# Clear the oled display in case it has junk on it.
oled.fill(0)

# Blit the image from the framebuffer to the oled display


# Add some text
# oled.text("Raspberry Pi",5,5)
# oled.pixel(30,30,1)
# oled.hline(0,42,128,42)  # Draw Line
# oled.vline(0, 0, 64, 1) #vertical line
# oled.rect(0, 0, 128, 64,1)
# oled.fill_rect(0, 0, 64, 32, 1)
timer = Timer()
flag = False
def blink(timer):
    if flag:        
        display_welcome()
    else:
        temp_display()
    

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)

def display_welcome():
    oled.fill(0)
    font_writer = writer.Writer(oled, freesans20)    
    font_writer.set_textpos(0, 0)
    font_writer.printstring("{}".format("MICRO"))
    font_writer.set_textpos(25, 25)
    font_writer.printstring("{}".format("PYTHON"))
    oled.show()
    
def temp_display():
    oled.fill(0)
    pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    t  = (sensor.temperature)
    h = (sensor.humidity)
    oled.rect(0, 0, 128, 64,1)
    oled.vline(63, 0, 128, 1) #vertical line
    oled.blit(fb, 2, 2)
    oled.blit(fb1, 64, 2)    
    font_writer = writer.Writer(oled, freesans20)    
    font_writer.set_textpos(4, 38)
    font_writer.printstring("{}%".format(str(h)))
    font_writer.set_textpos(66, 38)
    font_writer.printstring("{}C".format(str(t)))
    oled.show()
    
while True:
    if flag :
        flag = False
    else:
        flag = True
    time.sleep(2)

# Finally update the oled display so the image & text is displayed

       
    
    
    
    






