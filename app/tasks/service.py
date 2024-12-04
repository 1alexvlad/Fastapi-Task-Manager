from fastapi import HTTPException
from sqlalchemy import select
from app.service.base import BaseService
from app.tasks.models import Category, Tasks
from app.tasks.schemas import CategoryBase
from app.database import async_session_maker

class CategoryService(BaseService):
    model = Category

    @classmethod
    async def create_category(cls, category_data: CategoryBase) -> Category:
        async with async_session_maker() as session:
            existing_category = await session.execute(
                select(Category).where(Category.id == category_data.id)
            )
            if existing_category.scalars().first() is not None:
                raise HTTPException(status_code=400, detail='Такой ID уже существует.')

            new_category = Category(**category_data.dict())
            session.add(new_category)
            try:
                await session.commit()
                await session.refresh(new_category)
            except:
                await session.rollback()
                raise HTTPException(status_code=400, detail='Ошибка при добавление категории')    

            return new_category 

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




class TastService(BaseService):
    model = Tasks