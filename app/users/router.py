from jose import JWTError, jwt

from typing import List
from fastapi import APIRouter, HTTPException, Request, Response, status, Depends

from app.users.dependencies import get_current_user
from app.users.schemas import SUser, SUserRegister, SUserLogin
from app.users.service import UserService
from app.users.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token
from app.users.models import Users
from app.config import settings


router = APIRouter(
    prefix='/user',
    tags=['Пользователь']
)


@router.get('', summary='Получить всех пользователей')
async def get_all_users() -> List[SUser]:
    return await UserService.find_all()


@router.post('/register')
async def register_user(user_data: SUserRegister):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(
        email=user_data.email, password=hashed_password, 
        first_name=user_data.first_name, last_name=user_data.last_name, age=user_data.age
    )
    return {'message': 'Вы успешно зарегистрировались'}


@router.post('/login')
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({'sub': str(user.id)})
    refresh_token = await create_refresh_token({'sub': str(user.id)})
    response.set_cookie("user_access_token", access_token, httponly=True)
    response.set_cookie("user_refresh_token", refresh_token, httponly=True)
    return {'message': 'Вход успешно выполнен'}

@router.post('/refresh-token')
async def refresh_token(response: Response, request: Request):
    refresh_token = request.cookies.get('user_refresh_token') 
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token не найден')
    
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id: str = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
        new_access_token = create_access_token({'sub': str(user_id)})
        response.set_cookie('user_access_token', new_access_token, httponly=True)
        
        return {'access_token': new_access_token}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный refresh token')


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('user_access_token')
    response.delete_cookie('user_refresh_token')
    return {'message': 'Пользователь вышел из системы'}


@router.get('/me')
async def read_user_me(current_user: Users = Depends(get_current_user)) -> SUser:
    return current_user