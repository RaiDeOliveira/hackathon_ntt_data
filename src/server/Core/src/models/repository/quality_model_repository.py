from typing import Dict, List
from src.models.settings.connection import db_connection_handler
from src.models.entities.quality import Quality
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

class QualityRepository:
  def insert_quality(self, sensorInfo) -> Dict:
    with db_connection_handler as database:
      try:
        sensor = Quality(
          ibtug=sensorInfo.get("ibtug"),
          humidity=sensorInfo.get("humidity"),
          lux=sensorInfo.get("lux"),
          noise=sensorInfo.get("noise"),
          peopleNumber = sensorInfo.get("peopleNumber"),
          ErgonomicsIndex = sensorInfo.get("ErgonomicsIndex"),
          QualityIndex = sensorInfo.get("QualityIndex")
        )

        database.session.add(sensor)
        database.session.commit()

        return sensorInfo
      
      except IntegrityError:
        raise Exception("Sensor already exists!")

      except Exception as exception:
        database.session.rollback()
        raise exception
      
  def get_all_quality(self) -> List[Dict]:
    with db_connection_handler as database:
        try:
          sensors = database.session.query(Quality).all()
          return [sensor.to_dict() for sensor in sensors]
        except NoResultFound:
          return []
        except Exception as exception:
          raise exception