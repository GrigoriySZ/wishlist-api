from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Связи
    wishlists: Mapped[list['Wishlist']] = relationship('Wishlist', back_populates='user')
    booked_items: Mapped[list['Item']] = relationship('Item', back_populates='user')


class Wishlist(Base):
    __tablename__ = 'wishlists'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)

    # Связи
    user: Mapped['User'] = relationship('User', back_populates='wishlists')
    wishlist_items: Mapped[list['Item']] = relationship('Item', back_populates='wishlist', lazy='selectin')

class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    wishlist_id: Mapped[int] = mapped_column(Integer, ForeignKey('wishlists.id'), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False)
    booked_by_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)

    # Связи
    user: Mapped['User'] = relationship('User', back_populates='booked_items')
    wishlist: Mapped['Wishlist'] = relationship('Wishlist', back_populates='wishlist_items', lazy='selectin')
