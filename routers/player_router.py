from fastapi import HTTPException, APIRouter, Depends, Body
from typing import Annotated
from passlib.context import CryptContext
from starlette import status
from database import db_dependency
from models import Players
from routers.auth_router import get_current_player
from classes import ResetPasswordValidation

router = APIRouter(
    tags=["player"],
    prefix="/player"
)

# DEPENDENCIES
player_dependency = Annotated[dict, Depends(get_current_player)]

#BCRYPT CONFIG
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FOR THE LOGGED AS PLAYER, GET HIS INFOS
@router.get("/", status_code=status.HTTP_200_OK)
async def get_player(player: player_dependency, db: db_dependency):
    if player is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed.")
    return db.query(Players).filter(Players.id == player["id"]).first()

# LOGGED PLAYER CAN CHANGE HIS PASSWORD
@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(player: player_dependency, db: db_dependency, player_form_data: ResetPasswordValidation = Body()):
    if player is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed.")
    found_player = db.query(Players).filter(Players.id == player["id"]).first()
    if not bcrypt_context.verify(player_form_data.old_password, found_player.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authentication failed.")
    found_player.hashed_password = bcrypt_context.hash(player_form_data.new_password)
    db.add(found_player)
    db.commit()

