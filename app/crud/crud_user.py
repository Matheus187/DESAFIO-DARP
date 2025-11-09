from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash 


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    
    plain_password = user_in.password

    hashed_password = get_password_hash(plain_password)

    db_user = User(
        **user_in.model_dump(exclude={"password"}), 
        hash_password=hashed_password  
    )
    
   
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def delete(db: Session, *, db_obj: User) -> User:
    db.delete(db_obj)
    return db_obj

def get_first_admin(db: Session) -> User | None:
    return db.query(User).filter(User.role == UserRole.ADMIN).first()