import json
import paho.mqtt.client as paho
from paho import mqtt
import asyncio
from src.websocket.websocket_manager import websocket_manager
from src.models.repository.sensor_repository import SensorRepository

sensor_repository = SensorRepository()

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    message = msg.payload.decode('utf-8')

    try:
        sensor_data = json.loads(message)
        sensor_repository.insert_sensor(sensor_data)
        loop = asyncio.get_event_loop()
        loop.create_task(websocket_manager.broadcast(message))
    except json.JSONDecodeError:
        print("Error decoding JSON")
    except Exception as e:
        print(f"Error processing message: {e}")

def start_mqtt():
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect

    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("admin", "1234")
    client.connect("7b428a1c01224439a29d0f5558e645c3.s1.eu.hivemq.cloud", 8883)

    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    client.subscribe("daddyLion/#", qos=1)
    client.loop_start()
