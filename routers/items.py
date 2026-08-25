from fastapi import APIRouter, Depends, HTTPException ,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from typing import List
from schemas import ItemCreate, ItemRead, ItemBook
from models import Item, Wishlist, User

router = APIRouter(tags=['Управление подарками'])

# POST /wishlists/{wishlist_id}/items
@router.post('/wishlists/{wishlist_id}/items',
    response_model=List[ItemRead],
    status_code=status.HTTP_201_CREATED,
    summary="Добавить подарок в список желаний",
    description='Создает объект Item и привязывает его к объекту Wishlist по ID'
)
async def add_item(wishlist_id: int, items: List[ItemCreate], 
                   db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id))
    wishlist = result.scalar_one_or_none()
    if not wishlist: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f'Вишлист с ID {wishlist_id} не найден')

    create_items = []
    for item in items:
        new_item = Item(
            wishlist_id=wishlist_id,
            title=item.title,
            price=item.price
        )
        db.add(new_item)
        create_items.append(new_item)
    await db.flush()
    for item in create_items:
        await db.refresh(item)
    await db.commit()
    return create_items

# PATCH /items/{item_id}/book
@router.patch('/items/{item_id}/book', response_model=ItemRead,
              summary='Бронирует подарок за пользователем',
              description='')
async def book_item_by_id(item_id: int, 
                          book_data: ItemBook,
                          db: AsyncSession = Depends(get_db)
):
    item_query = await db.execute(select(Item).where(Item.id == item_id))
    item = item_query.scalar_one_or_none()
    if not item: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Подарок с ID {item_id} не найден')

    user_query = await db.execute(select(User).where(User.id == book_data.user_id))
    user = user_query.scalar_one_or_none()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пользователь с ID {book_data.user_id} на найден')

    if item.is_booked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Подарок уже забронирован')

    item.is_booked = True
    item.booked_by_user_id = book_data.user_id
    await db.flush()
    await db.refresh(item)
    await db.commit()
    return item

# DELETE /items/{item_id}
@router.delete('/items/{item_id}',
               status_code=status.HTTP_200_OK,
               summary='Удаляет подарок',
               description='Удалет объект Item по ID из базы данных и возвращает сообщение')
async def remove_item_from_db(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пожелание с ID {item_id} не найдена')

    await db.delete(item)
    await db.commit()

    return {'detail': f'Пожелание с ID {item_id} успешно удалена'}