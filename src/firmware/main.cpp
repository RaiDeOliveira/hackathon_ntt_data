#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define SEALEVELPRESSURE_HPA (1013.25)

// Configurações do Wi-Fi
const char* ssid = "sugarzero";      // Insira o SSID do seu Wi-Fi
const char* password = "sugarzero"; // Insira a senha do seu Wi-Fi
const char* mqtt_server = "mqtt-dashboard.com"; // Host do Broker MQTT
const char* mqtt_topic = "daddyLion"; // Tópico para publicar
const char* mqtt_client_id = "client-id-sugarzero"; // Client ID

WiFiClient espClient;
PubSubClient client(espClient);

Adafruit_BME280 bme; // I2C

unsigned long delayTime;

void setup() {
  Serial.begin(9600);
  Serial.println(F("BME280 test"));

  // Conecta ao Wi-Fi
  setup_wifi();
  
  // Conecta ao Broker MQTT
  client.setServer(mqtt_server, 1883);

  bool status;
  status = bme.begin(0x76);  
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }

  delayTime = 1000;
}

void loop() {
  // Verifica a conexão com o MQTT
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Coleta e publica os dados
  publishValues();
  
  delay(delayTime);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando-se ao Wi-Fi ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop até se conectar ao MQTT
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    
    if (client.connect(mqtt_client_id)) {
      Serial.println("Conectado");
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void publishValues() {
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();

  // Publica temperatura e umidade no formato JSON
  String payload = "{\"temperature\": ";
  payload += String(temperature);
  payload += ", \"humidity\": ";
  payload += String(humidity);
  payload += "}";

  Serial.print("Publicando mensagem: ");
  Serial.println(payload);

  // Publica no tópico MQTT
  client.publish(mqtt_topic, (char*) payload.c_str());
}
