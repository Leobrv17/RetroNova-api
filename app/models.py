from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from data_base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    publique_id = Column(String(12), unique=True, nullable=False)
    firebase_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    nb_ticket = Column(Integer, default=0, nullable=False)
    bar = Column(Boolean, default=False, nullable=False)

    __table_args__ = (UniqueConstraint('publique_id', 'firebase_id'),)

    # Relation vers un modèle Payments (exemple)
    payments = relationship("Payments", back_populates="user")


# Table Games
class Games(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    nb_max_player = Column(Integer, nullable=False)


# Table Arcade_machines
class ArcadeMachines(Base):
    __tablename__ = "arcade_machines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    description = Column(String(255), nullable=True)
    localisation = Column(String(255), nullable=True)
    game1_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    game2_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=True)

    game1 = relationship("Games", foreign_keys=[game1_id])
    game2 = relationship("Games", foreign_keys=[game2_id])


# Table Friends
class Friends(Base):
    __tablename__ = "friends"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    friend_from_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    friend_to_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    accept = Column(Boolean, default=False, nullable=False)
    decline = Column(Boolean, default=False, nullable=False)
    delete = Column(Boolean, default=False, nullable=False)

    # Relations
    friend_from = relationship("Users", foreign_keys=[friend_from_id])
    friend_to = relationship("Users", foreign_keys=[friend_to_id])

    __table_args__ = (
        UniqueConstraint("friend_from_id", "friend_to_id", name="unique_friendship"),
    )


# Table Payments
class Payments(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_stripe_token = Column(String, unique=True, nullable=False)
    amount = Column(Integer, nullable=False)
    nb_ticket = Column(Integer, nullable=False)

    # Relation
    user = relationship("Users", back_populates="payments")


# Table Parties
class Parties(Base):
    __tablename__ = "parties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    player1_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    player2_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    machine_id = Column(UUID(as_uuid=True), ForeignKey("arcade_machines.id"), nullable=False)
    total_score = Column(Integer, nullable=True)
    p1_score = Column(Integer, nullable=True)
    p2_score = Column(Integer, nullable=True)
    password = Column(Integer, nullable=True)
    done = Column(Boolean, default=False, nullable=False)
    cancel = Column(Boolean, default=False, nullable=False)
    bar = Column(Boolean, nullable=True)

    # Relations
    player1 = relationship("Users", foreign_keys=[player1_id])
    player2 = relationship("Users", foreign_keys=[player2_id])
    game = relationship("Games")
    machine = relationship("ArcadeMachines")
