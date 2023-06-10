# class Caijin(Base):
#     __tablename__ = 'admin_member_caijin'
#     id          = Column(Integer,      comment='ID', unique=True, primary_key=True, )
#     member_id   = Column(Integer, ForeignKey("admin_member.id", ondelete='CASCADE', onupdate='CASCADE'))
#     members     = relationship("Member", back_populates="caijins", lazy='joined',  passive_deletes=True)
#     # source    = 彩金来源
#     money       = Column(DECIMAL(10,2), comment="彩金金额")
#     description = Column(String(255),  comment='备注', index=True)
#     first_name  = Column(String(255),  comment='创建者')
#     last_name   = Column(String(255),  comment='最后一次更新者')
#     created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
#     updated_at  = Column(TIMESTAMP(timezone=True))

from pydantic import BaseModel,Field
from typing import Optional,List,Union



class CreateMemberCaiJinSchema(BaseModel):
    member_id: int
    source_id: int
    money: Union[int, float] = Field(..., ge=0, le=2400000000)
    description: Optional[str] = None





class batchDeleteMemberCaiJinSchema(BaseModel):
    ids: Optional[List] = []



class batchImportMemberCaiJinSchema(BaseModel):
    importData: Optional[List] = []
