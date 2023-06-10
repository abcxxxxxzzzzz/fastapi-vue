from pydantic import BaseModel
from typing import Union


class UpdateGroupStatusSchema(BaseModel):
    status: int

class CreateGroupSchema(UpdateGroupStatusSchema):
    name: str
    description: Union[str, None]  = None



class UpdateGroupSchema(BaseModel):
    name: str
    description: Union[str, None]  = None




# class GroupOutSchema(CreateGroupSchema):
#     id: int
#     create_at: datetime
#     update_at: datetime

    
#     class Config:
#         orm_mode = True