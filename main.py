from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routers import users, wishlists, items
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield 

app = FastAPI(
    title='Вишлист подарков API',
    description='RESTful API для ведения удобных вишлистов подарков',
    version='1.0.0',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(users.router)
app.include_router(wishlists.router)
app.include_router(items.router)

@app.get('/', tags=['Служебное'])
async def root():
    return {'message': 'Добро пожаловать в сервис Вишлист подарков'}