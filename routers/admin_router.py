from fastapi import HTTPException, APIRouter, Depends, Path
from typing import Annotated
from starlette import status
from database import db_dependency
from models import Heroes
from  routers.auth_router import get_current_player

router = APIRouter(
    tags=["admin"],
    prefix="/admin",
)

# DEPENDENCIES
player_dependency = Annotated[dict, Depends(get_current_player)]

# GET ALL (FOR THE LOGGED AS ADMIN)
@router.get("/heroes", status_code=status.HTTP_200_OK)
async def get_all_heroes(player: player_dependency, db: db_dependency):
    if player is None or player["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed.")
    return db.query(Heroes).order_by(Heroes.id.asc()).all()

# DELETE (BY ID AS PATH PARAM) (FOR THE LOGGED AS ADMIN)
@router.delete("/delete/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(player: player_dependency, db: db_dependency, hero_id: int = Path(ge=1)):
    if player is None or player["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed.")
    hero_db = db.query(Heroes).filter(Heroes.id == hero_id).first()
    if hero_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero can't be found.")
    db.delete(hero_db)
    db.commit()