from pydantic import BaseModel
from typing import List,Union,Optional




class CreateKeyWordSchema(BaseModel):
    name: str
    type: Union[str,None] = None
    status: Union[int,None] = -2


class batchCreateKeyWordSchema(BaseModel):
    batchContent: Union[List[dict], str] = None
    type: str



class batchDeleteKeyWordSchema(BaseModel):
    ids: Optional[List] = []


class batchUpdataKeyWordSchema(batchDeleteKeyWordSchema):
    status: int


class batchConditionUpdataKeyWordSchema(BaseModel):
    status: int