from typing import List
from fastapi import APIRouter, HTTPException
from app.users.schemas import SUser
from app.users.service import UserService

router = APIRouter(
    prefix='/user',
    tags=['Пользователь']
)


@router.get('', summary='Получить всех пользователей')
async def get_all_users() -> List[SUser]:
    return await UserService.find_all()


@router.get('/{id}', summary='Получить пользоваетеля по id')
async def get_by_id_user(id: int) -> SUser:
    user = await UserService.find_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user