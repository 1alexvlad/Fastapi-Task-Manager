from fastapi import FastAPI

from app.users.router import router as user_router
from app.tasks.router import router_category
from app.tasks.router import router_task


app = FastAPI()


app.include_router(user_router)
app.include_router(router_category)
app.include_router(router_task)