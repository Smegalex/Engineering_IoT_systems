import time
from counterfit_shims_seeed_python_dht import DHT
from counterfit_connection import CounterFitConnection
import paho.mqtt.client as mqtt
import json


minute = 1  # 60


CounterFitConnection.init('127.0.0.1', 5000)

sensor = DHT("11", 106)

id = "604b0228-9053-48c7-97ас-30а3с7dcса57"
client_name = id + 'temperature_sensor_client'
client_telemetry_topic = id + '/telemetry'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")

while True:
    _, temp = sensor.read()
    telemetry = json.dumps({'temperature': temp})

    print("Sending telemetry:", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(10 * minute)
