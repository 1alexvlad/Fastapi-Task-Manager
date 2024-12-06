from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

from app.tasks.models import Priority, Status


class TaskBase(BaseModel):
    id: int
    date: date
    title: str = Field(..., min_length=1, max_length=100, description="Имя от 1 до 100 символов")
    description: Optional[str] = None
    category_id: int
    priority: str
    status: str
    user_id: int

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    date: date
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category_id: int
    priority: Priority 
    status: Status   
    user_id: int


class TaskUpdate(BaseModel):
    date: date
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category_id: int
    priority: Priority 
    status: Status   
    user_id: int



class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
