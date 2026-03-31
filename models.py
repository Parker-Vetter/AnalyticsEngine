from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class PlayerStats(Base):
    __tablename__ = "player_stats"

    id         = Column(Integer, primary_key=True, index=True)
    player_id  = Column(String, index=True)
    total_kills = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())