from pydantic import BaseModel
from typing import Union,Optional,List




class CreateRecordOutMoneySchema(BaseModel):
    owner_id: int
    uid: str
    bank_name: str
    bank_owner: str
    bank_child: Union[str, None] = None
    bank_card: str
    out_money: str




class UpdateRecordOutMoneyStatusSchema(BaseModel):
    status: int


class ChangeDescriptionRecordOutMoneySchema(BaseModel):
    description: Union[str, None] = None

class DoneRecordOutMoneySchema(ChangeDescriptionRecordOutMoneySchema):
    img_path: Union[str, None] = None
    rece: int

    
class batchDeleteRecordOutMoneySchema(BaseModel):
    ids: Optional[List] = []
