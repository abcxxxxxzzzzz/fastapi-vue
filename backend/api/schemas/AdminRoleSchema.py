from pydantic import BaseModel
from typing import Union,List,Optional





class UpdateRoleStatusSchema(BaseModel):
    status: int


class CreateRoleSchema(UpdateRoleStatusSchema):
    name: str
    description: Optional[str] = None
    permissions: Optional[List] = []


class UpdateRoleSchema(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Optional[List] = []


# class RoleOutSchema(CreateRoleSchema):
#     id: int
#     create_at: datetime
#     update_at: datetime
#     user: List[str] = []
#     permission: List

    
#     class Config:
#         orm_mode = True



class RoleBindPermissionSchema(BaseModel):
    permissions: List[int] = []

