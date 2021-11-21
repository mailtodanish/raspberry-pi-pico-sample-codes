from machine import Pin, Timer
import utime as time
from pico_i2c_lcd import I2cLcd
from machine import I2C
from dht import DHT11, InvalidChecksum

timer = Timer()
i2c = I2C(id=0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
led = Pin(15, Pin.OUT)
led_red = Pin(14, Pin.OUT)
led_red.high()
led_red.high()

Green = True
Red = False
def blink(timer):
    if Green:
        led.toggle()
    else:
        led.low()
    if Red:
        led_red.toggle()
    else:
        led_red.low()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)

while True:
    
        pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
        sensor = DHT11(pin)
        t  = (sensor.temperature)
        h = (sensor.humidity)
        if t > 25 :
            Green= True
            Red=False
        else:
            Green= True
            Red=True
        
            
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr('Temp :')
        lcd.move_to(7,0)
        lcd.putstr(str(t)+" C")
        lcd.move_to(0,1)
        lcd.putstr('Humidity :')
        lcd.move_to(10,1)
        lcd.putstr(str(h)+"%")
        time.sleep(5)
        lcd.clear()
        lcd.hide_cursor()
    
    
    
    
    





