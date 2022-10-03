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

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    master_name = Column(VARCHAR(255), nullable=False)
    open = Column(Integer, nullable=False)
    close = Column(Integer, nullable=False)
    dinner = Column(Integer, nullable=False)

    def __str__(self):
        return f"{self.date} - {self.master_name}: {self.open} - {self.close}"

    def __init__(self, date, master_name, open_day, close, dinner):
        self.date = date
        self.master_name = master_name
        self.open = open_day
        self.close = close
        self.dinner = dinner


class Master(BaseModel):
    __tablename__ = "master"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100), nullable=False)

    def __init__(self, name):
        self.name = name


class Admin(BaseModel):
    __tablename__ = "admin_list"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(VARCHAR(100), nullable=False)

    def __init__(self, id, username):
        self.user_id = id
        self.username = username

    def __str__(self):
        return self.username


class Record(BaseModel):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    master = Column(VARCHAR(100), nullable=False)
    record_time = Column(Integer, nullable=False)
