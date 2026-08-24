from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas import WishlistCreate, WishlistRead
from models import Wishlist, User

router = APIRouter(prefix='/wishlists', tags=['Управление списками подарков'])

# POST /wishlists
@router.post('/', response_model=WishlistCreate, status_code=status.HTTP_201_CREATED)
async def create_new_wishlist(wishlist_data: WishlistCreate, 
                              db: AsyncSession = Depends(get_db)) -> Wishlist:
    query = select(User).where(User.id == wishlist_data.user_id)
    result = await db.execute(query)

    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Пользователь с ID {wishlist_data.user_id} не найден')

    new_wishlist = Wishlist(
        user_id=wishlist_data.user_id,
        title=wishlist_data.title
    )
    db.add(new_wishlist)
    await db.flush()
    await db.refresh(new_wishlist)
    await db.commit()

    return new_wishlist

# GET /wishlists/{wishlist_id}
@router.get('/{wishlist_id}', response_model=WishlistRead)
async def get_wishlist_by_id(wishlist_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Wishlist).options(
        selectinload(Wishlist.wishlist_items)).filter(Wishlist.id == wishlist_id)
    result = await db.execute(query)

    wishlist = result.scalar_one_or_none()
    if not wishlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Список подарков с ID {wishlist_id} не найден')

    return wishlist