import datetime
from src.models.settings.base import Base
from sqlalchemy import Column, Integer, Float, DateTime

class Sensor(Base):
  __tablename__ = 'sensor'
  
  id = Column(Integer, primary_key=True)
  temperature = Column(Float)
  humidity = Column(Float)
  lux = Column(Float)
  noise = Column(Float)
  timestamp = Column(DateTime, default=datetime.datetime.utcnow)
  
  def __repr__(self):
    return "Sensor(id={}, temperature={}, humidity={}, lux={}, noise={}, timestamp={})".format(
      self.id,
      self.temperature,
      self.humidity,
      self.lux,
      self.noise,
      self.timestamp
    )

  def to_dict(self):
      return {
          "id": self.id,
          "temperature": self.temperature,
          "humidity": self.humidity,
          "lux": self.lux,
          "noise": self.noise,
          "timestamp": self.timestamp.isoformat() if self.timestamp else None
      }
      