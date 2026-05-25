from typing import List, Annotated, Optional, Literal
from pydantic import BaseModel, Field, constr, field_validator

fieldStr = Annotated[str, Field(min_length=3)]

class Hero:
    id: int
    nick_name: str
    full_name: str
    occupation: List[str]
    powers: List[int]
    hobby: List[str]
    type: str
    rank: int

    def __init__(self, id, nick_name, full_name, occupation, powers, hobby, type, rank):
        self.id = id
        self.nick_name = nick_name
        self.full_name = full_name
        self.occupation = occupation
        self.powers = powers
        self.hobby = hobby
        self.type = type
        self.rank = rank

class HeroValidation(BaseModel):
    id: Optional[int] = Field(default=None, gt=0)
    nick_name: str = Field(min_length=3)
    full_name: str = Field(min_length=3)
    occupation: List[fieldStr]
    powers: List[fieldStr]
    hobby: List[fieldStr]
    type: str = Field(min_length=3)
    rank: int = Field(ge=0, le=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "nick_name": "Percy",
                "full_name": "Gale Dekariou Percial",
                "occupation": ["Wizard", "Adventurer", "Deity"],
                "powers": ["Magical prowess", "High intelligence", "Charisma"],
                "hobby": ["Studying magic", "Drinking", "Cooking"],
                "type": "Wizard",
                "rank": 65,

            }
        }
    }

AllowedRoles = Literal["controller", "defender", "leader", "striker"]

class PlayerValidation(BaseModel):
    email: str = Field(description="Mail address")
    username: str = Field(description="Pseudo")
    first_name: str = Field(description="First name")
    last_name: str = Field(description="Family name")
    password: str = Field(description="Password")
    role: AllowedRoles = Field(description="Role of the player. Should be either controller, defender, leader or striker")
    # PRE VALIDATOR
    @field_validator("role", mode="before")
    @classmethod
    def lower_case_role(cls, val: str) -> str:
        return val.lower()

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "player1@mail.com",
                "username": "pl1",
                "first_name": "pl1",
                "last_name": "pl1",
                "password": "123&zErT!",
                "role": "controller",
            }
        }
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class ResetPasswordValidation(BaseModel):
    old_password: str = Field(description="Old password")
    new_password: str = Field(description="New password")