import uuid
from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.database import get_async_session
from app.models.models import Menu, Submenu
from app.schemas import schemas

menus_router = APIRouter(prefix='/api/v1')


@menus_router.get('/menus', response_model=list[schemas.MenuOut])
async def get_list_menus(session: AsyncSession = Depends(get_async_session)) -> Sequence[Menu]:
    res = await session.execute(select(Menu).options(selectinload(Menu.submenus)))
    return res.scalars().all()


@menus_router.get('/menus/{menu_id}', response_model=schemas.MenuOut)
async def get_menu_by_id(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(
        select(Menu)
        .options(selectinload(Menu.submenus).joinedload(Submenu.dishes))
        .where(Menu.id == menu_id)
    )
    menu = res.scalars().one_or_none()
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@menus_router.post('/menus', response_model=schemas.MenuOut, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: schemas.MenuIn, session: AsyncSession = Depends(get_async_session)) -> Menu:
    new_menu = Menu(id=uuid.uuid4(), title=menu.title, description=menu.description)
    session.add(new_menu)
    await session.commit()

    res = await session.execute(
        select(Menu).options(selectinload(Menu.submenus)).where(Menu.id == new_menu.id)
    )
    return res.scalars().one_or_none()


@menus_router.patch('/menus/{menu_id}', response_model=schemas.MenuOut)
async def update_menu_by_id(
        menu: schemas.MenuIn,
        menu_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
) -> Menu:
    res = await session.execute(
        select(Menu)
        .options(selectinload(Menu.submenus).joinedload(Submenu.dishes))
        .where(Menu.id == menu_id)
    )
    result = res.scalars().one_or_none()
    result.title = menu.title
    result.description = menu.description

    await session.commit()

    return result


@menus_router.delete('/menus/{menu_id}')
async def delete_menu_by_id(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)) -> dict:
    res = await session.execute(select(Menu).where(Menu.id == menu_id))
    result = res.scalars().one_or_none()

    await session.delete(result)
    await session.commit()

    return {
        'status': True,
        'message': 'The menu has been deleted'
    }
