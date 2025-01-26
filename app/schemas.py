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
    description: Optional[str]
    localisation: Optional[str]
    game1_id: UUID
    game2_id: Optional[UUID]

class ArcadeMachineCreate(ArcadeMachineBase):
    pass

class ArcadeMachineUpdate(BaseModel):
    description: Optional[str]
    localisation: Optional[str]
    game1_id: Optional[UUID]
    game2_id: Optional[UUID]

class ArcadeMachineResponse(ArcadeMachineBase):
    id: UUID

    class Config:
        orm_mode = True


# Games Schema
class GameBase(BaseModel):
    name: str
    description: Optional[str] = None
    nb_max_player: int

class GameCreate(GameBase):
    pass

class GameUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    nb_max_player: Optional[int]

class GameResponse(GameBase):
    id: UUID

    class Config:
        orm_mode = True


# Friends Schema
class FriendsBase(BaseModel):
    friend_from_id: UUID
    friend_to_id: UUID
    accept: bool = False
    decline: bool = False
    delete: bool = False

class FriendsCreate(FriendsBase):
    pass

class FriendsUpdate(BaseModel):
    accept: bool = None
    decline: bool = None
    delete: bool = None

class FriendsResponse(FriendsBase):
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

class PaymentUpdate(BaseModel):
    session_stripe_token: Optional[str]
    amount: Optional[int]
    nb_ticket: Optional[int]

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
    total_score: Optional[int] = None
    p1_score: Optional[int] = None
    p2_score: Optional[int] = None
    password: Optional[int] = None
    done: bool = False
    cancel: bool = False
    bar: Optional[bool] = None

class PartyCreate(PartyBase):
    pass

class PartyUpdate(BaseModel):
    total_score: Optional[int] = None
    p1_score: Optional[int] = None
    p2_score: Optional[int] = None
    password: Optional[int] = None
    done: Optional[bool] = False
    cancel: Optional[bool] = False
    bar: Optional[bool] = None

class PartyResponse(PartyBase):
    id: UUID

    class Config:
        orm_mode = True