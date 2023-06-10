from pydantic import BaseModel
from typing import List,Union,Optional




class CreateWeightSchema(BaseModel):
    name: str
    status: Union[int,None] = -2
    type: str



class batchCreateWeightSchema(BaseModel):
    batchContent: Union[List[dict], str] = None
    batchType: str



class batchDeleteWeightSchema(BaseModel):
    ids: Optional[List] = []



class batchUpdataWeightSchema(batchDeleteWeightSchema):
    status: int


class batchConditionUpdataWeightSchema(BaseModel):
    status: int