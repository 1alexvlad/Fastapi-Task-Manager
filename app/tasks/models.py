from enum import Enum
from sqlalchemy import String, Integer, Column, Text, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base
from app.users.models import Users



class Priority(str, Enum):
    low = 'Низкий'
    middle = 'Средний'
    high = 'Высокий'


class Status(str, Enum):
    done = 'Выполнена'
    not_done = 'Не выполнена'


class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    tasks = relationship("Tasks", back_populates="category")



class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(ForeignKey('category.id'), nullable=False)
    priority = Column(String, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)

    category = relationship("Category", back_populates="tasks")
    user = relationship('Users', back_populates='tasks')