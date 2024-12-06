from enum import Enum
from fastapi import HTTPException
from sqlalchemy import select
from app.service.base import BaseService
from app.tasks.models import Category, Tasks
from app.tasks.schemas import CategoryBase, CategoryCreate, TaskBase, TaskCreate, TaskUpdate
from app.database import async_session_maker

class CategoryService(BaseService):
    model = Category

    @classmethod
    async def create_category(cls, category_data: CategoryCreate) -> CategoryBase:
        async with async_session_maker() as session:
            new_category = cls.model(name=category_data.name)
            session.add(new_category)
            try:
                await session.commit()
                await session.refresh(new_category)
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail=f'Ошибка при добавлении задачи: {str(e)}')
            return CategoryBase.model_validate(new_category) 


    @classmethod
    async def delete_category(cls, id: int):
        async with async_session_maker() as session:
            category_query = select(Category).where(Category.id == id)
            result = await session.execute(category_query)
            category = result.scalars().first()

            if not category:
                raise HTTPException(status_code=404, detail='ID категории не найдена')
            
            await session.delete(category)
            await session.commit()


class TaskService(BaseService):
    model = Tasks

    @classmethod
    async def create_task(cls, task_data: TaskCreate) -> TaskBase:
        async with async_session_maker() as session:
            new_task = cls.model(
                date=task_data.date,
                title=task_data.title,
                description=task_data.description,
                category_id=task_data.category_id,
                priority=task_data.priority,
                status=task_data.status,
                user_id=task_data.user_id
            )
            
            session.add(new_task)
            try:
                await session.commit()
                await session.refresh(new_task)
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail=f'Ошибка при добавлении задачи')

            return TaskBase.model_validate(new_task) 
        
    @classmethod
    async def delete_task(cls, id: int):
        async with async_session_maker() as session:
            find_delete_task = select(Tasks).where(Tasks.id == id)
            result = await session.execute(find_delete_task)
            task = result.scalars().first()

            if not task:
                raise HTTPException(status_code=404, detail='ID не найдено')
            await session.delete(task)
            await session.commit()

    @classmethod
    async def update_task(cls, id: int, task_data: TaskUpdate) -> TaskBase: 
        async with async_session_maker() as session:
            find_task = select(Tasks).where(Tasks.id == id)
            result = await session.execute(find_task)
            task = result.scalars().first()
            
            if not task:
                raise HTTPException(status_code=404, detail='ID не найдено')
            
            task.date = task_data.date
            task.title = task_data.title
            task.description = task_data.description
            task.category_id = task_data.category_id
            task.priority = task_data.priority
            task.status = task_data.status
            task.user_id = task_data.user_id

            session.add(task)

            try:
                await session.commit()
                await session.refresh(task) 

            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail='Ошибка при обновлении задачи')

            return TaskBase.model_validate(task)  