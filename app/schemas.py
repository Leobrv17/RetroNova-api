from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional
from uuid import UUID
from datetime import datetime
import re

# Users Schema
class UserBase(BaseModel):
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    nb_ticket: int = Field(0)
    bar: Optional[bool] = Field(False)

class UserCreate(UserBase):
    firebase_id: str

class UserResponse(UserBase):
    id: UUID
    publique_id: str
    firebase_id: str

    class ConfigDict :
        model_config = ConfigDict(from_attributes = True)


# Arcade Machines Schema
class ArcadeMachineBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    localisation: Optional[str] = None
    game1_id: Optional[UUID] = None
    game2_id: Optional[UUID] = None

class ArcadeMachineCreate(ArcadeMachineBase):
    name: str
    nb_player_min: int
    nb_player_max: int
    game1_id: UUID

class ArcadeMachineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    localisation: Optional[str] = None
    game1_id: Optional[UUID] = None
    game2_id: Optional[UUID] = None

class ArcadeMachineResponse(ArcadeMachineBase):
    id: UUID

    class Config:
        from_attributes = True


# Games Schema
class GameBase(BaseModel):
    name: str
    description: Optional[str] = None
    nb_max_player: int
    nb_min_player: int

class GameCreate(GameBase):
    pass

class GameUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    nb_max_player: Optional[int]
    nb_min_player: Optional[int]

class GameResponse(GameBase):
    id: UUID

    class ConfigDict :
        model_config = ConfigDict(from_attributes = True)


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

    class ConfigDict :
        model_config = ConfigDict(from_attributes = True)


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

    class ConfigDict :
        model_config = ConfigDict(from_attributes = True)

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

    class ConfigDict :
        model_config = ConfigDict(from_attributes = True)

#Promo code
class PromoCodeBase(BaseModel):
    code: str = Field(..., min_length=6, max_length=12)
    nb_parties: int = Field(1, gt=0)
    is_active: bool = Field(True)
    expires_at: Optional[datetime] = Field(None)
    max_uses: Optional[int] = Field(None, gt=0)

    @validator('code')
    def validate_code(cls, v):
        if not re.match(r'^[A-Za-z0-9]+$', v):
            raise ValueError('Le code promo doit être alphanumérique (lettres et chiffres uniquement)')
        return v.upper()  # Convertir en majuscules pour la cohérence

class PromoCodeCreate(PromoCodeBase):
    pass

class PromoCodeUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=6, max_length=12)
    nb_parties: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None
    max_uses: Optional[int] = Field(None, gt=0)

    @validator('code')
    def validate_code(cls, v):
        if v is None:
            return v
        if not re.match(r'^[A-Za-z0-9]+$', v):
            raise ValueError('Le code promo doit être alphanumérique (lettres et chiffres uniquement)')
        return v.upper()  # Convertir en majuscules pour la cohérence

class PromoCodeResponse(PromoCodeBase):
    id: UUID
    created_at: datetime
    used_count: int

    class ConfigDict:
        model_config = ConfigDict(from_attributes=True)

# Pour la vérification/utilisation du code promo
class PromoCodeUse(BaseModel):
    code: str = Field(..., min_length=6, max_length=12)
    user_id: UUID

class PromoCodeUsageResponse(BaseModel):
    success: bool
    message: str
    nb_parties: Optional[int] = None