from typing import List
from fastapi import APIRouter

from app.tasks.schemas import CategoryBase
from app.tasks.service import CategoryService


router = APIRouter(
    prefix='/category',
    tags=['Категория']
)

@router.get('', summary='Посмотреть все категории')
async def get_all_category() -> List[CategoryBase]:
    return await CategoryService.find_all()


@router.post('/add', summary='Добавить новую категорию')
async def create_category(category: CategoryBase) -> CategoryBase:
    created_category = await CategoryService.create_category(category)
    return created_category


@router.delete('/{id}', summary='Удалить категорию по id')
async def delete_category_by_id(id: int):
    await CategoryService.delete_category(id)
    return {'message': 'Категория успешно удалена.'}