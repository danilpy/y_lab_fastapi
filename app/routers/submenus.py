import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.database import get_async_session
from app.models.models import Submenu
from app.schemas import schemas

submenu_router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus')


@submenu_router.get('menus/{menu_id}/submenus', response_model=list[schemas.SubmenuOut])
async def get_list_submenus(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(Submenu).options(selectinload(Submenu.dishes)).where(Submenu.menu_id == menu_id))
    return res.scalars().all()


@submenu_router.get('menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubmenuOut, )
async def get_submenu_by_id(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
) -> Submenu:
    res = await session.execute(
        select(Submenu)
        .options(selectinload(Submenu.dishes))
        .where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
    )
    submenu = res.scalars().one_or_none()
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@submenu_router.post(
    'menus/{menu_id}/submenus',
    response_model=schemas.SubmenuOut,
    status_code=status.HTTP_201_CREATED
)
async def create_submenu(
        submenu: schemas.SubmenuIn,
        menu_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
) -> Submenu:
    new_menu = Submenu(id=uuid.uuid4(), title=submenu.title, description=submenu.description, menu_id=menu_id)
    session.add(new_menu)
    await session.commit()

    res = await session.execute(select(Submenu).options(selectinload(Submenu.dishes)).where(Submenu.id == new_menu.id))
    return res.scalars().one_or_none()


@submenu_router.patch('menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubmenuOut)
async def update_submenu_by_id(
        submenu: schemas.SubmenuIn,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session),
) -> Submenu:
    res = await session.execute(
        select(Submenu)
        .options(selectinload(Submenu.dishes))
        .where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
    )
    result = res.scalars().one_or_none()
    result.title = submenu.title
    result.description = submenu.description

    await session.commit()

    return result


@submenu_router.delete('menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu_by_id(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    res = await session.execute(
        select(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
    )
    result = res.scalars().one_or_none()

    await session.delete(result)
    await session.commit()

    return {
        'status': True,
        'message': 'The submenu has been deleted'
    }
