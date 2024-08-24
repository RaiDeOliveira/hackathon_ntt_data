#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define SEALEVELPRESSURE_HPA (1013.25)

// Configurações do Wi-Fi
const char* ssid = "sugarzero";      // Insira o SSID do seu Wi-Fi
const char* password = "sugarzero"; // Insira a senha do seu Wi-Fi
const char* mqtt_s#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <FS.h>
#include <LittleFS.h>

// Configurações de rede e MQTT
const char* ssid = "sugarzero";
const char* password = "sugarzero";
const char* mqtt_server = "7b428a1c01224439a29d0f5558e645c3.s1.eu.hivemq.cloud";
const int mqtt_port = 8883; // Porta segura
const char* mqtt_user = "admin"; // Usuário MQTT
const char* mqtt_pass = "1234";  // Senha MQTT

WiFiClientSecure espClient; // Usa WiFiClientSecure para conexão MQTT segura
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (500)
char msg[MSG_BUFFER_SIZE];
int value = 0;

// Definir o pino do LED embutido (normalmente é o pino 2 em muitas placas ESP32)
const int ledPin = 2;

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

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  
  // Acender LED se o payload não for nulo
  if (length > 0) {
    digitalWrite(ledPin, LOW); // Acender LED
    delay(500);
    digitalWrite(ledPin, HIGH); // Apagar LED
  } else {
    digitalWrite(ledPin, HIGH); // Apagar LED
  }
}

void reconnect() {
  // Loop até se reconectar
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    String clientId = "ESP32Client";
    
    // Tenta conectar com usuário e senha
    if (client.connect(clientId.c_str(), mqtt_user, mqtt_pass)) {
      Serial.println("Conectado ao MQTT");
      // Publica mensagem inicial
      client.publish("daddyLion", "Olá mundo");
      // Inscreve-se no tópico
      client.subscribe("daddyLion");
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  delay(500);

  // Inicializa LittleFS e força a formatação se necessário
  if (!LittleFS.begin(true)) { // O parâmetro true força a formatação
    Serial.println("Falha ao montar o LittleFS, formatando...");
    return;
  }

  setup_wifi();

  // Inicializa o pino do LED embutido como saída
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH); // Garante que o LED começa apagado

  // Configura o cliente MQTT
  espClient.setInsecure(); // Desativa verificação de certificado (modo inseguro)
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf(msg, MSG_BUFFER_SIZE, "Olá mundo #%ld", value);
    Serial.print("Publicando mensagem: ");
    Serial.println(msg);
    client.publish("daddyLion", msg);
  }
}
erver = "mqtt-dashboard.com"; // Host do Broker MQTT
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
