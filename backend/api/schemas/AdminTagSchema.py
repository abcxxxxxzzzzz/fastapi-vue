from pydantic import BaseModel



class CreateTagSchema(BaseModel):
    name: str
    color: str
