from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Metric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String(128), nullable=False)
    status = Column(String(32), nullable=False)
    response_time_ms = Column(Float, nullable=True)
    error_rate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'service': self.service,
            'status': self.status,
            'response_time_ms': self.response_time_ms,
            'error_rate': self.error_rate,
            'created_at': self.created_at.isoformat() + 'Z',
        }
