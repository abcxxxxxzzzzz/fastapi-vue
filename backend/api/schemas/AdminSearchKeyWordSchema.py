from pydantic import BaseModel
from typing import Optional,List,Union




class CreateSearchKeyWordSchema(BaseModel):
    number: int
    link: str
    url_website: str
    contact: str
    cn: Union[str, None] = None
    en: Union[str, None] = None
    color: Union[str, None] = None
    owner_id: str
    description: Union[str, None] = None


class LockSearchKeyWordSchema(BaseModel):
    is_contact: int



class BatchCreateSearchKeyWordSchema(BaseModel):
    owner_id: str
    data: Optional[List] = []




class batchDeleteSearchKeyWordSchema(BaseModel):
    ids: Optional[List] = []
