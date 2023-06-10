from pydantic import BaseModel



class CreateWebTagSchema(BaseModel):
    name: str
    color: str
