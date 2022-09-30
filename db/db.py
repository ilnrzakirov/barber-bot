from sqlalchemy import (
    VARCHAR,
    Column,
    Date,
    Integer,
)
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class HairDay(BaseModel):
    __tablename__ = "hair_days"

    date = Column(Date, nullable=False)
    master_name = Column(VARCHAR(255), nullable=False)
    open = Column(Integer, nullable=False)
    close = Column(Integer, nullable=False)
    dinner = Column(Integer, nullable=False)

    def __str__(self):
        return f"{self.date} - {self.master_name}: {self.open} - {self.close}"
