from fastapi import FastAPI, Query, Path, Body, HTTPException
from sqlalchemy import text
from starlette import status
from database import db_dependency
from classes import HeroValidation, Hero
from heroes import HEROES
from utils import find_proper_hero_id

app = FastAPI()
@app.get("/")
async def heartbeat(db: db_dependency):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "DATABASE OK"}
    except Exception as e:
        return {"error": str(e)}


# GET ALL
@app.get("/heroes", status_code=status.HTTP_200_OK)
async def get_all_heroes():
    return HEROES

# GET BY TYPE (AS QUERY PARAM)
@app.get("/heroes/type", status_code=status.HTTP_200_OK)
async def get_heroes_by_type(hero_type: str = Query()):
    result = []
    for hero in HEROES:
        if hero_type.casefold() == hero.type.casefold():
            result.append(hero)
    return result


# GET BY RANK (AS QUERY PARAM)
@app.get("/heroes/rank", status_code=status.HTTP_200_OK)
async def get_heroes_by_rank(hero_rank: int = Query(ge=0, le=100)):
    result = []
    for hero in HEROES:
        if hero.rank >= hero_rank:
            result.append(hero)
    return result


# GET BY ID (AS PATH PARAM)
@app.get("/hero/id/{hero_id}", status_code=status.HTTP_200_OK)
async def get_one_hero_by_id(hero_id: int = Path(gt=0)):
    for hero in HEROES:
        if hero.id == hero_id:
            return hero
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero can't be found.")


# GET BY NICKNAME (AS PATH PARAM)
@app.get("/hero/nick/{nick}", status_code=status.HTTP_200_OK)
async def get_one_hero_by_nick(nick: str = Path()):
    for hero in HEROES:
        if nick.casefold() == hero.nick_name.casefold():
            return hero
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero can't be found.")


# POST/CREATE (BY BODY)
@app.post("/hero/create", status_code=status.HTTP_201_CREATED)
async def create_hero(hero_body: HeroValidation = Body()):
    new_hero   = Hero(**hero_body.model_dump())
    HEROES.append(find_proper_hero_id(new_hero))


# UPDATE WITH PUT (BY BODY)
@app.put("/hero/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_hero(hero_body: HeroValidation = Body()):
    hero_changed = False
    for i in range(len(HEROES)):
        if HEROES[i].id == hero_body.id:
           hero_changed = True
           HEROES[i] = Hero(**hero_body.model_dump())
    if not hero_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero can't be found.")


# DELETE (BY ID AS PATH PARAM)
@app.delete("/hero/delete/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(hero_id: int = Path(gt=0)):
    hero_changed = False
    for i in range(len(HEROES)):
        if HEROES[i].id == hero_id:
           hero_changed = True
           HEROES.pop(i)
           break
    if not hero_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero can't be found.")

