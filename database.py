from typing import Annotated
from fastapi.params import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/DungeonsAndDragons"

# DEF ENGINE (moteur de connexion à la base)
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# DEF OF SESSION (l'usine à session pour créer des sessions de R/W en BD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DEF OF BASE AS AN OBJECT TO USE (Modèle parent de tous les modèles de tables ecrit dans le fastApi)
Base = declarative_base()

#  DEPENDENCY CORE
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DEPENDENCY ANNOTATED
db_dependency = Annotated[Session, Depends(get_db)]