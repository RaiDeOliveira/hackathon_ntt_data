from typing import Dict, List
from src.models.settings.connection import db_connection_handler
from src.models.entities.sensor import Sensor
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


class SensorRepository:
  def insert_sensor(self, sensorInfo) -> Dict:
    with db_connection_handler as database:
      try:
        sensor = Sensor(
          temperature=sensorInfo.get("temperature"),
          humidity=sensorInfo.get("humidity"),
          lux=sensorInfo.get("lux"),
          noise=sensorInfo.get("noise")
        )

        database.session.add(sensor)
        database.session.commit()

        return sensorInfo
      
      except IntegrityError:
        raise Exception("Sensor already exists!")

      except Exception as exception:
        database.session.rollback()
        raise exception
      
  def get_all_sensors(self) -> List[Dict]:
    with db_connection_handler as database:
        try:
          sensors = database.session.query(Sensor).all()
          return [sensor.to_dict() for sensor in sensors]
        except NoResultFound:
          return []
        except Exception as exception:
          raise exception