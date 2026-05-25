import os
from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Body, APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from starlette.middleware import Middleware

from classes import PlayerValidation, Token
from database import db_dependency
import models
from models import Players
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    tags=["auth"],
    prefix="/auth",
)

# BEARER TOKEN DEPENDENCY FOR THE ENDPOINTS
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

#BCRYPT CONFIG
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT CONFIG
# KEY GENERATED WITH COMMAND: openssl rand -hex 64
JWT_SECRET_KEY = "70188626c959da57ff626b348e07933daf5c1a4f65c5de3ce8c992cd2a64b384f654d8102a6769dcd3c5f57a887b4331474bd41c3a68e92fba0cdcae0da8e1af"
JWT_ALGO = "HS256"

# HELPER FUNCTION FOR LOGIN
def authenticate_player(username: str, password: str, db):
    found_player = db.query(Players).filter(Players.username == username).first()
    if not found_player:
        return False
    if not bcrypt_context.verify(password, found_player.hashed_password):
        return False
    return found_player

def create_token(username: str, user_id: int, expires_delta: timedelta):
    encoded_data = {"sub": username, "id": user_id}
    expiration = datetime.now(timezone.utc) + expires_delta
    encoded_data.update({ "exp": expiration.timestamp() })
    return jwt.encode(encoded_data, JWT_SECRET_KEY, algorithm=JWT_ALGO)
##

# FOR AUTH MIDDLEWARE
async def get_current_player(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGO])
        username: str = payload["sub"]
        user_id: int = payload["id"]
        if  not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong credentials")
##


@router.post("/register", status_code=status.HTTP_201_CREATED)
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

@router.post("/login", response_model= Token, status_code=status.HTTP_200_OK)
async def  login_player(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    player_authenticated = authenticate_player(form_data.username, form_data.password, db)
    if not player_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials")
    token = create_token(player_authenticated.username, player_authenticated.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}