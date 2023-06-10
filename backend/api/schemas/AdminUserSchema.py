from pydantic import BaseModel, constr, Field
from typing import Union,List,Optional
from datetime import datetime



class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    description: Optional[str] = None
    avatar: Optional[str] = None
    status: Optional[int] = None
    # roles: Optional[List] = []
    # groups: Optional[List] = []
    role_id: Optional[List] = []
    group_id: Optional[List] = []

class CreateUserSchema(UserBase):
    password: str = Field(..., min_length=3, max_length=50)
    

class UpdateUserPwdSchema(BaseModel):
    oldpassword: str
    password: str = Field(..., min_length=3, max_length=50)
    repassword: str = Field(..., min_length=3, max_length=50)



class UpdateUserSchema(BaseModel):
    description: Optional[str] = None
    avatar: Optional[str] = None
    password: Union[str, None] = None
    # roles: Optional[List] = []
    # groups: Optional[List] = []
    role_id: Optional[List] = []
    group_id: Optional[List] = []



class UpdateUserStatusSchema(BaseModel):
    status: int



# class UserOutSchema(UserBase):
#     id: int
#     is_super: int
#     # groups: List[GroupOutSchema]
#     # role: List[RoleOutSchema]
#     create_at: datetime
#     update_at: datetime

    
#     class Config:
#         orm_mode = True


class UserBindGroupSchema(BaseModel):
    groups: List[int] = []


class UserBindRoleSchema(BaseModel):
    roles: List[int] = []