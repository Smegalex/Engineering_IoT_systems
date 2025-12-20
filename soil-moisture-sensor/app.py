import time
import json
from counterfit_shims_grove.adc import ADC
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_relay import GroveRelay
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse, X509

host_name = "soil-moisture-sensor-oleksandr-tunik.azure-devices.net"
device_id = "soil-moisture-sensor-x509-oleksandr-tunik"
x509 = X509("./soil-moisture-sensor-x509-oleksandr-tunik-cert.pem",
            "./soil-moisture-sensor-x509-oleksandr-tunik-key.pem")


device_client = IoTHubDeviceClient.create_from_x509_certificate(x509,
                                                                host_name, device_id)
print('Connecting')
device_client.connect()
print('Connected')


CounterFitConnection.init('127.0.0.1', 5000)

adc = ADC()
relay = GroveRelay(107)


def handle_method_request(request):
    print("Direct method received - ", request.name)
    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)


device_client.on_method_request_received = handle_method_request

while True:
    try:
        soil_moisture = adc.read(106)
    except Exception as e:
        print(f"Error reading sensor: {e}")
    print(f"Soil moisture: {soil_moisture}")
    message = Message(json.dumps({'soil_moisture': soil_moisture}))
    device_client.send_message(message)

    time.sleep(10)
