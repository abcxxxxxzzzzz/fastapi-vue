
from pydantic import BaseModel,conint
from typing import List,Optional
from datetime import datetime



class UpdatePermissionStatusSchema(BaseModel):
    status: int


class CreatePermissionSchema(UpdatePermissionStatusSchema):
    name: str
    menu: Optional[int] = None
    code: Optional[str] = None
    frontpath: Optional[str] = None
    method: Optional[str] = None
    icon:   Optional[str] = None
    sort: conint(ge=0)
    parent_id: Optional[int] = None
    


class UpdatePermissionSchema(BaseModel):
    name: str
    menu: Optional[int] = None
    code: Optional[str] = None
    frontpath: Optional[str] = None
    method: Optional[str] = None
    icon:   Optional[str] = None
    sort: conint(ge=0)
    parent_id: Optional[int] = None
    
    




# class PermissionOutSchema(CreatePermissionSchema):
#     id: int
#     create_at: datetime
#     update_at: datetime
#     role: List

    
#     class Config:
#         orm_mode = True