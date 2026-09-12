from datetime import datetime

from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.orm import Mapped,mapped_column

from database import Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True,index=True)
    username: Mapped[str] = mapped_column(String(50),nullable=False,unique=True)
    email: Mapped[str] = mapped_column(String(100),nullable=False,unique=True)
    password: Mapped[str] = mapped_column(String(100),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
  