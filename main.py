from fastapi import FastAPI
from database import engine
import models
from routers import heroes_router, auth_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(heroes_router.router)
app.include_router(auth_router.router)
