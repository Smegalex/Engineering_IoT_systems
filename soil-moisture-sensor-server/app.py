import json
import time
import threading
import paho.mqtt.client as mqtt

id = '8d15a2d7-258e-4955-824f-875c02b45292'
client_telemetry_topic = id + '/telemetry'
client_name = id + 'soil_moisture_sensor_server'
server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

water_time = 5
wait_time = 20


def send_relay_command(client, state):
    command = {'relay_on': state}
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))


def control_relay(client):
    print("Unsubscribing from telemetry")
    mqtt_client.unsubscribe(client_telemetry_topic)
    send_relay_command(client, True)
    time.sleep(water_time)
    send_relay_command(client, False)
    time.sleep(wait_time)
    print("Subscribing to telemetry")
    mqtt_client.subscribe(client_telemetry_topic)


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    if payload['soil_moisture'] > 881:
        threading.Thread(target=control_relay, args=(client,)).start()


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry


while True:
    time.sleep(2)
