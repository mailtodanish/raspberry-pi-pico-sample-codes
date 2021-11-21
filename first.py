print('Hello Pico Temprature!')
from machine import Pin, ADC, Timer
import utime
sensor_temp = ADC(4)
conversion_factor = 3.3/(65535)
led = Pin(25, Pin.OUT)

tim = Timer()
def tick(timer):
    global led
    led.toggle()
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    print("Temprature: " , temperature)
   

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
