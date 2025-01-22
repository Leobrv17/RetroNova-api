from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

# Users Schema
class UserBase(BaseModel):
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    nb_ticket: int = Field(0)
    bar: Optional[bool] = Field(False)

class UserCreate(UserBase):
    firebase_id: UUID

class UserResponse(UserBase):
    id: UUID
    publique_id: str
    firebase_id: UUID

    class Config:
        orm_mode = True


# Arcade Machines Schema
class ArcadeMachineBase(BaseModel):
    description: Optional[str] = Field(None, max_length=255)
    localisation: Optional[str] = Field(None, max_length=255)

class ArcadeMachineCreate(ArcadeMachineBase):
    game1_id: Optional[UUID]
    game2_id: Optional[UUID]

class ArcadeMachineResponse(ArcadeMachineBase):
    id: UUID
    game1_id: Optional[UUID]
    game2_id: Optional[UUID]

    class Config:
        orm_mode = True


# Games Schema
class GameBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    nb_max_player: Optional[int]

class GameCreate(GameBase):
    pass

class GameResponse(GameBase):
    id: UUID

    class Config:
        orm_mode = True


# Friends Schema
class FriendBase(BaseModel):
    friend_from_id: UUID
    friend_to_id: UUID
    accept: Optional[bool] = Field(False)
    decline: Optional[bool] = Field(False)

class FriendCreate(FriendBase):
    pass

class FriendResponse(FriendBase):
    id: UUID

    class Config:
        orm_mode = True


# Payments Schema
class PaymentBase(BaseModel):
    user_id: UUID
    session_stripe_token: str
    amount: int
    nb_ticket: int

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: UUID

    class Config:
        orm_mode = True


# Parties Schema
class PartyBase(BaseModel):
    player1_id: UUID
    player2_id: UUID
    game_id: UUID
    machine_id: UUID
    total_score: Optional[int]
    p1_score: Optional[int]
    p2_score: Optional[int]
    password: Optional[int]
    done: Optional[bool] = Field(False)
    cancel: Optional[bool] = Field(False)
    bar: Optional[bool]

class PartyCreate(PartyBase):
    pass

class PartyResponse(PartyBase):
    id: UUID

    class Config:
        orm_mode = True