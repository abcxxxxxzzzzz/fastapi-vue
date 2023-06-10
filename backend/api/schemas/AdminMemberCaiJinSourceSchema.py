from pydantic import BaseModel



class CreateMemberCaiJinSourceSchema(BaseModel):
    name: str
    color: str
