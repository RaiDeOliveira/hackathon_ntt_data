import datetime
from src.models.settings.base import Base
from sqlalchemy import Column, Integer, Float, DateTime,INTEGER

class Quality(Base):
  __tablename__ = 'quality'
  
  id = Column(Integer, primary_key=True)
  ibtug = Column(Float)
  humidity = Column(Float)
  lux = Column(Float)
  noise = Column(Float)
  peopleNumber = Column(INTEGER)
  ErgonomicsIndex = Column(Float)
  QualityIndex = Column(Float)
  timestamp = Column(DateTime, default=datetime.datetime.utcnow)
  
  def __repr__(self):
    return "Quality(id={}, ibtug={}, humidity={}, lux={}, noise={},peopleNumber,ErgonomicsIndex,QualityIndex, timestamp={})".format(
      self.id,
      self.ibtug,
      self.humidity,
      self.lux,
      self.noise,
      self.peopleNumber,
      self.ErgonomicsIndex,
      self.QualityIndex,
      self.timestamp
    )

  def to_dict(self):
      return {
          "id": self.id,
          "temperature": self.temperature,
          "humidity": self.humidity,
          "lux": self.lux,
          "noise": self.noise,
          "ErgonomicsIndex":self.ErgonomicsIndex,
          "QualityIndex":self.QualityIndex,
          "peopleNumber":self.peopleNumber,
          "timestamp": self.timestamp.isoformat() if self.timestamp else None
      }
      