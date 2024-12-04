from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

from app.tasks.models import Priority, Status


class TaskBase(BaseModel):
    date: date
    title: str = Field(..., min_length=1, max_length=100, description="Имя от 1 до 100 символов")
    description: Optional[str] = None
    priority: Priority
    status: Status


class TaskCreate(TaskBase):
    category_id: int


class Task(TaskBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True  



class CategoryBase(BaseModel):
    id: int
    name: str


    class Config:
        orm_mode = True