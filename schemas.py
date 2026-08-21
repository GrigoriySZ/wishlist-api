from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List

class UserCreate(BaseModel): 
    username: str = Field(..., min_length=1, max_length=64, description='Имя или никнейм пользователя')

class UserRead(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=64, description='Название позиции в вишлисте')
    price: Optional[int] = Field(default=None, validate_default=True, description='Цена позиции в вишлисте')

    @field_validator('price')
    @classmethod
    def validate_price(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value < 0:
            raise ValueError('Цена не может быть отрицательной')
        return value

class ItemRead(BaseModel):
    id: int
    title: str
    print: Optional[int]
    is_booked: bool
    booked_by_user_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class ItemBook(BaseModel):
    user_id: int = Field(..., description='ID пользователя, бронирующего позицию в вишлисте')

class WishlistCreate(BaseModel):
    user_id: int = Field(..., description='ID пользователя, создающего вишлист')
    title: str = Field(..., min_length=1, max_length=64, description='Название вишлиста')

class WishlistRead(BaseModel):
    id: int
    title: str
    user_id: int
    items: List[ItemRead] = []

    model_config = ConfigDict(from_attributes=True)