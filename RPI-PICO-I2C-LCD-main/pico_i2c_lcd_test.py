from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
i2c = I2C(id=0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
devices = i2c.scan()
print(devices)
if len(devices) == 0:
  print("I2C Address      : No I2C devices found")
else:
  print("I2C Address      : "+hex(devices[0]))
lcd.putstr("danish")
while True:
    print("t:")
    lcd.clear()
    lcd.putstr("danish")
    sleep(2)