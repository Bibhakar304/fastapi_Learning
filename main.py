import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session
from Routes.UserRoutes import router

from database import get_db

app = FastAPI(title="My API", description="This is a sample API", version="1.0.0"  )
logger = logging.getLogger(__name__)


app.include_router(router)

@app.get("/")
def get_root():
    return{"message":"Welcome to My API!"  }

# @app.post("/users")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     get_User = create_user_record(db=db, user=user)
#     if get_User is None:
#         return JSONResponse(status_code=500, content={"detail": "Failed to create user"})
#     else:
#         return JSONResponse(status_code=201, content={"detail": "User created successfully", "user_id": get_User.user_id})  
#     return get_User

# @app.get("/users/{user_id}")
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = get_user_by_id(db=db, user_id=user_id)
#     if user is None:
#         return JSONResponse(status_code=404, content={"detail": "User not found"})
#     return user