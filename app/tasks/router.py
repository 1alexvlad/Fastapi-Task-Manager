from typing import List
from fastapi import APIRouter, HTTPException

from app.tasks.schemas import CategoryBase, CategoryCreate, TaskBase, TaskCreate, TaskUpdate
from app.tasks.service import CategoryService, TaskService


router_category = APIRouter(
    prefix='/category',
    tags=['Категория']
)

router_task = APIRouter(
    prefix='/task',
    tags=['Задачи']
)

@router_category.get('', summary='Посмотреть все категории')
async def get_all_category() -> List[CategoryBase]:
    return await CategoryService.find_all()

@router_category.get('/{id}', summary='Получить id категории')
async def get_category_by_id(id: int) -> CategoryBase:
    category = await CategoryService.find_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@router_category.post('', response_model=CategoryBase , summary='Добавить новую категорию')
async def create_category(category: CategoryCreate) -> CategoryBase:
    return await CategoryService.create_category(category)


@router_category.delete('/{id}', summary='Удалить категорию по id')
async def delete_category_by_id(id: int):
    await CategoryService.delete_category(id)
    return {'message': 'Категория успешно удалена.'}



@router_task.get('', summary='Получить все задачи')
async def get_all_tasks() -> List[TaskBase]:
    return await TaskService.find_all()

@router_task.get('/{id}', summary='Получить задачу по id')
async def get_task_by_id(id: int) -> TaskBase:
    task = await TaskService.find_by_id(id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@router_task.post('', response_model=TaskBase, summary='Добавить новую задачу')
async def create_task(task: TaskCreate) -> TaskBase:
    return await TaskService.create_task(task)

@router_task.delete('/{id}', summary='Удалить задачу по id')
async def delete_task_by_id(id: int):
    await TaskService.delete_task(id)
    return {'message': 'Task удалена'}


@router_task.patch('/{id}', response_model=TaskBase, summary='Обновить задачу по ID')
async def update_task(id: int, task_data: TaskUpdate) -> TaskBase:
    existing_task = await TaskService.find_by_id(id)
    if not existing_task:
        raise HTTPException(status_code=404, detail='Задача не найдена')

    updated_task = await TaskService.update_task(id, task_data)
    return updated_task