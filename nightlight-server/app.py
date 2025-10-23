import json
import time
import paho.mqtt.client as mqtt

id = 'ebbd0880-d8d8-4f6c-837a-e90b10aad89f'
client_name = id + 'nightlight_server'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("Connected to mosquitto")


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    command = {'led_on': payload['light'] < 106}

    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)
