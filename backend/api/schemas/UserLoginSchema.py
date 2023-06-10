from pydantic import BaseModel
from typing import List, Optional

class LoginSchema(BaseModel):
    username: str
    password: str



class LoginUser(BaseModel):
    id: str
    username: str
    roles: Optional[List[dict]] = []
    permissions: Optional[List[str]] = []
    loginTime: str
    # visitTime: str
    # expireTime: str



class Token(BaseModel):
    token: str