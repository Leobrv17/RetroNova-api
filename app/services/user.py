import uuid
from sqlalchemy.orm import Session

from models import Users
from schemas import  UserCreate



def generate_unique_id(db: Session):
    while True:
        new_id = str(uuid.uuid4().int)[:12]

        existing_user = db.query(Users).filter_by(publique_id=new_id).first()
        if not existing_user:
            return new_id

def create_user(db: Session, user : UserCreate):
    unique_pub_id = generate_unique_id(db)
    db_user = Users(**user.dict(), publique_id=unique_pub_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

