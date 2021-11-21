from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidChecksum



while True:
    time.sleep(5)
    pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    print("Temperature: {}".format(sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))