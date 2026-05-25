from fastapi import Query, Path, Body, HTTPException, APIRouter
from sqlalchemy import text
from starlette import status
from database import db_dependency, engine
from classes import HeroValidation
import models
from models import Heroes

router = APIRouter(
    tags=["heroes"],
    prefix="/heroes",
)

models.Base.metadata.create_all(bind=engine)

@router.get("/heartbeat", status_code=status.HTTP_200_OK)
async def heartbeat(db: db_dependency):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "DATABASE OK"}
    except Exception as e:
        return {"error": str(e)}


# GET ALL
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_heroes(db: db_dependency):
    return db.query(Heroes).order_by(Heroes.id.asc()).all()

# GET BY TYPE (AS QUERY PARAM)
@router.get("/type", status_code=status.HTTP_200_OK)
async def get_heroes_by_type(db: db_dependency, hero_type: str = Query()):
    result = db.query(Heroes).filter(Heroes.type.ilike(f"%{hero_type}%")).all()
    return result


# GET BY RANK (AS QUERY PARAM)
@router.get("/rank", status_code=status.HTTP_200_OK)
async def get_heroes_by_rank(db: db_dependency, hero_rank: int = Query(ge=0, le=100)):
    result = db.query(Heroes).filter(Heroes.rank >= hero_rank).all()
    return result


# GET BY ID (AS PATH PARAM)
@router.get("/id/{hero_id}", status_code=status.HTTP_200_OK)
async def get_one_hero_by_id(db: db_dependency, hero_id: int = Path(gt=0)):
    hero_db = db.query(Heroes).filter(Heroes.id == hero_id).first()
    if hero_db is not None:
        return hero_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero can't be found.")


# GET BY NICKNAME (AS PATH PARAM)
@router.get("/nick/{nick}", status_code=status.HTTP_200_OK)
async def get_one_hero_by_nick(db: db_dependency, nick: str = Path()):
    result = db.query(Heroes).filter(Heroes.nick_name.ilike(f"%{nick}%")).all()
    return result


# POST/CREATE (BY BODY)
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_hero(db: db_dependency, hero_body: HeroValidation = Body()):
    new_hero = Heroes(**hero_body.model_dump(exclude={"id"}))
    db.add(new_hero)
    db.commit()

# UPDATE WITH PUT (BY PATH)
@router.put("/update/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_hero(db: db_dependency, hero_id: int = Path(ge=1), hero_body: HeroValidation = Body()):
    hero_db = db.query(Heroes).filter(Heroes.id == hero_id).first()
    if hero_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero can't be found.")
    hero_db.nick_name = hero_body.nick_name
    hero_db.full_name = hero_body.full_name
    hero_db.occupation = hero_body.occupation
    hero_db.powers = hero_body.powers
    hero_db.hobby = hero_body.hobby
    hero_db.type = hero_body.type
    hero_db.rank = hero_body.rank
    db.add(hero_db)
    db.commit()



# DELETE (BY ID AS PATH PARAM)
@router.delete("/delete/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(db: db_dependency, hero_id: int = Path(ge=1)):
    hero_db = db.query(Heroes).filter(Heroes.id == hero_id).first()
    if hero_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero can't be found.")
    db.delete(hero_db)
    db.commit()

