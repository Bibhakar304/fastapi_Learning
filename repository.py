# from sqlalchemy import select
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import Session
# from model import User
# from schemas import UserCreate


# def __int__(self,db:Session):
#     self.db = db

# def get_user_by_id(db:Session, user_id:int):
#     select_query = select(User).where(User.user_id == user_id)
#     result = db.execute(select_query).scalar_one_or_none()
#     return result
# def create_user(db:Session,user:UserCreate):
#     new_user = User(
#         username=user.username,
#         email = user.email,
#         password =user.password
#     )
#     db.add(new_user)
#     try:
#         db.commit()
#         db.refresh(new_user)
#         return new_user
#     except SQLAlchemyError:
#         db.rollback()
#         raise

