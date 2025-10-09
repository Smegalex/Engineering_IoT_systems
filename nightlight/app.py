from counterfit_connection import CounterFitConnection
import time
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

CounterFitConnection.init('127.0.0.1', 5000)

print('Hello World!')
light_sensor = GroveLightSensor(106)
led = GroveLed(107)
while True:
    light = light_sensor.light
    print('Light level:', light)
    if light < 300:
        led.on()
    else:
        led.off()
    time.sleep(1)
