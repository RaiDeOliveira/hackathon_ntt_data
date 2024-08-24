import paho.mqtt.client as mqtt
import logging
from src.config.settings import config
from src.websocket.websocket_manager import WebSocketManager

mqtt_config = config["mqtt"]
websocket_manager = WebSocketManager()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    logger.info("Connected to MQTT broker")
    client.subscribe(mqtt_config["topic"])
  else:
    logger.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, message):
  try:
    data = message.payload.decode()
    logger.info(f"Message received: {data}")
    print(data)
    
    websocket_manager.broadcast(data)
  except Exception as e:
    logger.exception(f"Error processing MQTT message: {str(e)}")

def start_mqtt():
  logger.info("Starting MQTT client")
  try:
    client = mqtt.Client(
      client_id=mqtt_config["client_id"], 
      clean_session=True, 
      userdata=None, 
      protocol=mqtt.MQTTv311, 
      transport="tcp"
    )
    logger.info(f"Connecting to {mqtt_config['broker_address']}:{mqtt_config['broker_port']}")
    
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_config["broker_address"], mqtt_config["broker_port"], mqtt_config["keep_alive"])
    client.loop_start()

    logger.info("MQTT Client started")
  except Exception as e:
    logger.exception(f"Error starting MQTT client: {str(e)}")

