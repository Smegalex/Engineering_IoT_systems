import time
import json
from counterfit_shims_grove.adc import ADC
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_relay import GroveRelay
import paho.mqtt.client as mqtt

CounterFitConnection.init('127.0.0.1', 5000)

adc = ADC()
relay = GroveRelay(107)

id = '8d15a2d7-258e-4955-824f-875c02b45292'
client_name = id + 'soil_moisture_sensor_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

print("MQTT connected!")


def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    if payload['relay_on']:
        relay.on()
    else:
        relay.off()


mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command


while True:
    try:
        soil_moisture = adc.read(106)
    except Exception as e:
        print(f"Error reading sensor: {e}")

    telemetry = json.dumps({'soil_moisture': soil_moisture})
    print("Sending telemetry:", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(10)
