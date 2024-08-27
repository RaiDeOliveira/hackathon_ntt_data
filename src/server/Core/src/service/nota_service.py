from src.models.repository.sensor_repository import SensorRepository
from src.websocket.websocket_client import get_websocket_client
from src.service.quality_model_service import calcule_and_save_quality_data
import json

class NotaService:
  def __init__(self):
    self.__sensor_repository = SensorRepository()
    self.__ws_client = get_websocket_client()

  async def dados_camera_ws(self):
    return self.__ws_client.get_last_message()


  async def qualityIndex(self):
    camera_ws = await self.dados_camera_ws()
    camera_ws = json.loads(camera_ws)
    calcule_and_save_quality_data()


  
