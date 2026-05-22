from fastapi import Body, APIRouter
from starlette import status
from passlib.context import CryptContext
from classes import PlayerValidation
from database import db_dependency
import models

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register_player(db: db_dependency, player_body: PlayerValidation = Body()):
    new_player = models.Players(
        email = player_body.email,
        username = player_body.username,
        first_name = player_body.first_name,
        last_name = player_body.last_name,
        hashed_password = bcrypt_context.hash(player_body.password),
        is_active = True,
        role = player_body.role
    )
    db.add(new_player)
    db.commit()