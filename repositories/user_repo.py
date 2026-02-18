
from models import User
from sqlalchemy.orm import Session

class UserRepo:
    def __init__(self,db:Session):
        self.db=db
    
    def add_user(self,user:User):
        self.db.add(user)
        self.db.commit()
        return user
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self,email:str):
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self):
        return self.db.query(User).all()
