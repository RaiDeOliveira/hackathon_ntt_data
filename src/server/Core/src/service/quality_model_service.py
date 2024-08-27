import asyncio
import json
from src.MathematicalModel.QualityIndex import QualityIndex
from src.models.repository.quality_model_repository import QualityRepository
from src.models.repository.sensor_repository import SensorRepository
import math
from src.websocket.websocket_client import get_websocket_client


quality_repository = QualityRepository()
sensor_repository = SensorRepository()
def calculate_Quality(current_angle,current_ibtug,current_noise,current_humidity,current_lux, current_peopleNumber,current_area):
    # angulos_atuais = {"braco": [19], "cabeça": [9]}
    angulos_atuais = current_angle
    angulos_ideais = {"braco": 20, "cabeça": 10}
    angulos_maximos = {"braco": 45, "cabeça": 25}
    pesos_articulacoes = {"braco": 0.2, "cabeça": 0.2}

    ibtug_atual = current_ibtug    
    ibtug_ideal = 20
    ibtug_max = 30
    peso_ibutg = 0.2


    ruido_atual = current_noise
    ruido_ideal = 50
    ruido_max = 85
    peso_ruido = 0.2

    luminosidade_atual = current_lux
    luminosidade_ideal = 500
    luminosidade_max = 1000
    peso_luminosidade = 0.1

    umidade_atual = current_humidity
    umidade_ideal = 50
    umidade_max = 70
    peso_umidade = 0.1

    lotacao_atual = current_peopleNumber
    lotacao_ideal = 10
    lotacao_max = 20
    peso_lotacao = 0.1
    area_sala = current_area

    quality_index = QualityIndex(angulos_atuais, angulos_ideais, angulos_maximos, pesos_articulacoes,
                                ibtug_atual, ibtug_ideal, ibtug_max, peso_ibutg, ruido_atual, ruido_ideal, ruido_max, peso_ruido,
                                        luminosidade_atual, luminosidade_ideal, luminosidade_max, peso_luminosidade,
                                        umidade_atual, umidade_ideal, umidade_max, peso_umidade,lotacao_atual, lotacao_ideal, lotacao_max, peso_lotacao,area_sala)


    # Cálculo do índice de qualidade
    indice_qualidade = quality_index.calcular_indice_qualidade()
    return quality_index

def calculateWetBulb(temperature, humidity):
        return temperature * math.atan(0.151977 * math.sqrt(humidity + 8.313659)) + 0.00391838 * math.sqrt(math.pow(humidity, 3)) * math.atan(0.023101 * humidity) - math.atan(humidity - 1.676331) + math.atan(temperature + humidity) - 4.686035
def calculateGlobeTemperature(temperature):
        return 0.456 + 1.0335 * temperature 
def calculate_ibutg(temperature,humidity):
    if temperature != None or humidity != None:
        return 0.7 * calculateWetBulb(temperature,humidity) + 0.3 * calculateGlobeTemperature(temperature)
    else: 
        return None
def calcule_and_save_quality_data(armAngle,headAngle,current_peopleNumber):
    CURRENT_AREA =20
    current_lux =500
    current_noise = 50
    current_peopleNumber =current_peopleNumber
    current_angle = {"braco":armAngle, "cabeça": headAngle}
    quality_data = quality_repository.get_all_quality()
    if len(quality_data)>0:
        sensor_data = [ {"ibutg":calculate_ibutg(i["temperature"],i["humidity"]),"humidity":i["humidity"],"timestamp":i["timestamp"]} for i in sensor_repository.get_all_sensors() if i["timestamp"] > quality_data[-1]["timestamp"]]
        for data in sensor_data:
             QIndex = calculate_Quality(current_angle,data["ibutg"],current_noise,data["humidity"],current_lux,current_peopleNumber,CURRENT_AREA)
             ergonomics_index = (1-QIndex.get_ErgonomicsIndex())*100
             quality_index_value =(1-QIndex.get_quality_index())*100
             q_data = { "ibtug":data["ibutg"],"humidity":data["humidity"],
                       "lux":current_lux,
                       "noise":current_noise,
                       "peopleNumber":current_peopleNumber,
                       "ErgonomicsIndex":ergonomics_index,
                       "QualityIndex":quality_index_value}
             quality_repository.insert_quality(q_data)

    else:
        sensor_data = [ {"ibutg":calculate_ibutg(i["temperature"],i["humidity"]),"humidity":i["humidity"],"timestamp":i["timestamp"]} for i in sensor_repository.get_all_sensors()]
        for data in sensor_data:
            quality_index = calculate_Quality(current_angle,data["ibutg"],current_noise,data["humidity"],current_lux,current_peopleNumber,CURRENT_AREA)
            QIndex = calculate_Quality(current_angle,data["ibutg"],current_noise,data["humidity"],current_lux,current_peopleNumber,CURRENT_AREA)
            ergonomics_index = (1-QIndex.get_ErgonomicsIndex())*100
            quality_index_value = (1-QIndex.get_quality_index())*100
            q_data = { "ibtug":data["ibutg"],"humidity":data["humidity"],
                       "lux":current_lux,
                       "noise":current_noise,
                       "peopleNumber":current_peopleNumber,
                       "ErgonomicsIndex":ergonomics_index,
                       "QualityIndex":quality_index_value}
            quality_repository.insert_quality(q_data)

