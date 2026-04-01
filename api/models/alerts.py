from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String(128), nullable=False)
    level = Column(String(32), nullable=False)
    message = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'service': self.service,
            'level': self.level,
            'message': self.message,
            'created_at': self.created_at.isoformat() + 'Z',
        }
