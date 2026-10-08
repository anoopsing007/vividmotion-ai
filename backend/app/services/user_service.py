from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserRegister
from app.services.security_service import SecurityService
import uuid

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserRegister) -> User:
        user_id = str(uuid.uuid4())
        hashed_password = SecurityService.hash_password(user_data.password)
        
        user = User(
            id=user_id,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            credits_remaining=10  # Free credits for new users
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def verify_password(db: Session, email: str, password: str) -> User | None:
        user = UserService.get_user_by_email(db, email)
        if user and SecurityService.verify_password(password, user.hashed_password):
            return user
        return None
    
    @staticmethod
    def deduct_credits(db: Session, user_id: str, amount: int) -> bool:
        user = UserService.get_user_by_id(db, user_id)
        if user and user.credits_remaining >= amount:
            user.credits_remaining -= amount
            db.commit()
            return True
        return False
