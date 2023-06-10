from pydantic import BaseModel
from typing import Optional,List,Union



class CreateWebSiteSchema(BaseModel):
    name: Union[str, None] = None
    child: Optional[List] = []
    channel_code: Union[str, None] = None
    contact: Optional[str] = None
    parent_id: Optional[str] = None
    wallet_address: Union[str, None] = None
    description: Union[str, None] = None
    tag_id: Optional[List] = []
    owner_id: int

    # 广告价格，广告位置，广告效果，OP链接
    gg_position: Union[str, None] = None
    gg_price: Union[str, None] = None
    gg_time: Union[str, None] = None
    gg_effect: Union[str, None] = None
    op_link: Union[str, None] = None 
    


class multideleteWebSiteSchema(BaseModel):
    ids: Optional[List] = []

class multiSearchWebSiteSchema(BaseModel):
    batchType: str
    batchContent: Union[List, str] = None
    includeDelete: int
    owner_id: Union[int, None] = None
    tag_id: Union[List, None] = None



class importWebSiteDataSchema(BaseModel):
    importData: Optional[List] = []