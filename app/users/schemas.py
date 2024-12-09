from pydantic import BaseModel, EmailStr, Field, field_validator



class SUser(BaseModel):
    id: int
    first_name: str = Field(..., min_length=1, max_length=50, description="Имя от 1 до 50 символов")
    last_name: str = Field(..., min_length=1, max_length=50, description="Фамилия от 1 до 50 символов")
    age: int = Field(..., ge=1, le=120, description='Возраст должен быть от 1 до 120')
    email: EmailStr = Field(..., description="Электронная почта студента")

class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str = Field(..., min_length=1, max_length=50, description="Имя от 1 до 50 символов")
    last_name: str = Field(..., min_length=1, max_length=50, description="Фамилия от 1 до 50 символов")
    age: int = Field(..., ge=1, le=120, description='Возраст должен быть от 1 до 120')

class SUserLogin(BaseModel):
    email: EmailStr
    password: str    