from pydantic import BaseModel
from typing import Generic,TypeVar

T= TypeVar("T")

class ApplicationResponce(BaseModel, Generic[T]):   
    StatusCode: int
    Message:str
    Data: T