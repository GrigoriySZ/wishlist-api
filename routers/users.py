from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import UserCreate, UserRead
from models import User
from typing import List

router = APIRouter(prefix='/users', tags=['Управление пользователями'])

# POST /users
@router.post('/', response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(username: str, db: AsyncSession = Depends(get_db)) -> User:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Пользователь с именем {username} уже существует'
        )

    new_user = User(username=username)
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    await db.commit()
    return new_user

# GET /users
@router.get('/', response_model=List[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    
    return users.scalars().all() 