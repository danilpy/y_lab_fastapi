import uvicorn
from fastapi import FastAPI

from app.routers.dishs import dish_router
from app.routers.menus import menus_router
from app.routers.submenus import submenu_router

app = FastAPI(
    title='YLab_University'
)

BASE_API_URL = '/api/v1/'

app.include_router(menus_router)
app.include_router(submenu_router)
app.include_router(dish_router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
