import paho.mqtt.client as mqtt
from src.config.settings import config

mqtt_config = config["mqtt"]

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Connected to broker")
    client.subscribe(mqtt_config["topic"])
  else:
    print("Connection failed")
    
def on_message(client, userdata, message):
  print(f"Message received: {message.payload.decode()}")
  
def start_mqtt():
  client = mqtt.Client(mqtt_config["client_id"])
  
  if mqtt_config.get("username") and mqtt_config.get("password"):
      client.username_pw_set(mqtt_config["username"], mqtt_config["password"])
  
  client.on_connect = on_connect
  client.on_message = on_message

  client.connect(mqtt_config["broker_address"], mqtt_config["broker_port"], mqtt_config["keep_alive"])

  client.loop_start()