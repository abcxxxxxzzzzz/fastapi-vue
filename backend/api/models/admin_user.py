from sqlalchemy import String,Integer,Column,Boolean,Table,ForeignKey,TIMESTAMP,text,Text,DECIMAL
from api.exts import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



# 创建中间表
admin_user_role = Table(
    "admin_user_role",  # 中间表名称
    Base.metadata,
    Column("user_id", Integer, ForeignKey("admin_user.id"), comment='用户编号'),  # 属性 外键
    Column("role_id", Integer, ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)



# 角色权限中间表
admin_role_permission = Table(
    "admin_role_permission",
    Base.metadata,
    Column("permission_id", Integer, ForeignKey("admin_permission.id"), comment='用户编号'),  # 属性 外键
    Column("role_id",       Integer, ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)


admin_user_group = Table(
    "admin_user_group",
    Base.metadata,
    Column("user_id",  Integer, ForeignKey("admin_user.id"), comment='用户编号'),  # 属性 外键
    Column("group_id", Integer, ForeignKey("admin_group.id"),   comment='部门编号'),  # 属性 外键
)
# ----------------------


# 用户表
class User(Base):
    __tablename__  = 'admin_user'
    id          = Column(Integer,  comment='ID', primary_key=True, index=True, )
    username    = Column(String(255),   comment="用户名", unique=True, index=True )
    password    = Column(String(255),   comment="密码")
    description = Column(String(255),   comment='描述')
    avatar      = Column(String(255),   comment='头像')
    status      = Column(Integer,  comment="是否有效", default=1 )
    is_super    = Column(Integer,  comment="是否超级管理员",default=0)
    created_at  = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    roles        = relationship('Role',   secondary=admin_user_role,    back_populates="users", lazy='joined', passive_deletes=True, order_by='Role.id')
    groups       = relationship('Group',  secondary=admin_user_group,   back_populates="users", lazy='joined', passive_deletes=True, order_by='Group.id')
    


# 角色表
class Role(Base):
    __tablename__ = 'admin_role'
    id          = Column(Integer,       comment='角色ID', primary_key=True, unique=True)
    name        = Column(String(255),   comment='角色名称', unique=True, index=True)
    description = Column(String(255),   comment='描述')
    status      = Column(Integer,       comment='是否有效')
    created_at  = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    users        = relationship('User',       secondary=admin_user_role,       back_populates="roles", lazy='dynamic', passive_deletes=True)
    permissions  = relationship("Permission", secondary=admin_role_permission, back_populates="roles", lazy='joined', passive_deletes=True, order_by='Permission.id')
    
    

# 权限表
class Permission(Base):
    __tablename__ = 'admin_permission'
    id         = Column(Integer,       comment='权限编号', unique=True, primary_key=True)
    name       = Column(String(255),   comment='权限名称', unique=True, index=True)
    menu       = Column(Integer,       comment='权限类型') # 1 是菜单，0 是按钮
    code       = Column(String(255),   comment='权限标识')
    frontpath  = Column(String(255),   comment='权限路径')
    method     = Column(String(255),   comment='请求方式')
    icon       = Column(String(255),   comment='图标')
    sort       = Column(Integer,       comment='排序')
    status     = Column(Integer,       comment='是否有效')
    parent_id  = Column(Integer,       comment='父类编号', default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    roles       = relationship('Role',   secondary=admin_role_permission,    back_populates="permissions", lazy='dynamic',passive_deletes=True)
    



# 组表
class Group(Base):
    __tablename__ = 'admin_group'
    id          = Column(Integer,      comment='组ID', unique=True, primary_key=True, )
    name        = Column(String(255),  comment='组名称', index=True, unique=True,)
    description = Column(String(255),   comment='描述')
    status      = Column(Integer,      comment='是否有效')
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    users       = relationship('User',  secondary=admin_user_group,  back_populates="groups", lazy='dynamic',passive_deletes=True)

    # 对应会员资料库
    members = relationship("Member", back_populates="owner", lazy='dynamic', order_by='Member.id')

    # 对应站点资料库
    websites = relationship("WebSite", back_populates="owner", lazy='dynamic', order_by='WebSite.id')
    

    # 对应会员信息库
    profiles = relationship("MemberProfile", back_populates="owner", lazy='dynamic', order_by='MemberProfile.id')


    # 对应出款
    outmoneys =  relationship('RecordOutMoney', back_populates="owner", lazy='dynamic', order_by='RecordOutMoney.id')


### ---  省的麻烦 --- Model 全写在一个文件里


admin_member_tag = Table(
    "admin_member_tag",
    Base.metadata,
    Column("member_id",  Integer, ForeignKey("admin_member.id"), comment='会员ID'),  # 属性 外键
    Column("tag_id", Integer, ForeignKey("admin_tag.id"),   comment='标签ID'),  # 属性 外键
)



admin_member_profile_tag = Table(
    "admin_member_profile_tag",
    Base.metadata,
    Column("profile_id",  Integer, ForeignKey("admin_member_profile.id"), comment='会员信息ID'),  # 属性 外键
    Column("tag_id", Integer, ForeignKey("admin_tag.id"),   comment='标签ID'),  # 属性 外键
)


# 会员标签
class Tag(Base):
    __tablename__ = 'admin_tag'
    id          = Column(Integer,      comment='ID', unique=True, primary_key=True, )
    name        = Column(String(255),  comment='标签名称', index=True, unique=True)
    color       = Column(String(255),  comment='标签颜色')
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    members     = relationship('Member',  secondary=admin_member_tag,   back_populates="tags", lazy='dynamic', passive_deletes=True)
    

    # 会信息资料多对多关联
    profiles    = relationship('MemberProfile',  secondary=admin_member_profile_tag,   back_populates="tags", lazy='dynamic', passive_deletes=True)




# 会员资料
class Member(Base):
    __tablename__ = 'admin_member'
    id           = Column(Integer,      comment='ID', unique=True, primary_key=True, )
    username     = Column(String(255),  comment='会员账户', index=True)
    channel_code = Column(String(255),  comment='渠道号', index=True)
    description = Column(String(255),  comment='备注', index=True)
    is_del      = Column(Integer, default=0, comment='是否已删除')
    first_name  = Column(String(255),  comment='创建者')
    last_name   = Column(String(255),  comment='更新者')
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))
    delete_at   = Column(TIMESTAMP(timezone=True))
    tags        = relationship('Tag',  secondary=admin_member_tag,   back_populates="members", lazy='joined',   passive_deletes=True)
    owner_id    = Column(Integer, ForeignKey("admin_group.id", ondelete='CASCADE', onupdate='CASCADE'))
    owner       = relationship("Group", back_populates="members", lazy='joined', order_by='Group.id', passive_deletes=True)


    total_in_money = Column(DECIMAL(24,2), comment="总存款金额", default=0,index=True)
    total_out_money = Column(DECIMAL(24,2), comment="总取款金额", default=0,index=True)
    total_caijin_money = Column(DECIMAL(24,2), comment="总彩金金额", default=0,index=True)   #自动计算
    total_before_two_in_money = Column(DECIMAL(24,2), comment="最近两个月存款金额",default=0, index=True)
    total_before_two_throw_money = Column(DECIMAL(24,2), comment="最近两个月投注金额",default=0, index=True)
    total_before_two_out_money = Column(DECIMAL(24,2), comment="最近两个月取款金额", default=0,index=True)
    total_before_two_wax_money = Column(DECIMAL(24,2), comment="最近两个月盈亏金额",default=0, index=True)
    total_wax_money = Column(DECIMAL(24,2), comment="总盈亏金额", default=0, index=True)
    register_at     = Column(TIMESTAMP(timezone=True), comment="注册时间")
    last_login_at   = Column(TIMESTAMP(timezone=True), comment="最后上线")
    register_ip     = Column(String(255), comment="注册IP")
    last_login_ip   = Column(String(255), comment="登录IP")



    caijins = relationship("MemberCaiJin", back_populates="members", lazy='joined',  passive_deletes=True)


# 彩金添加
# 归属部门      会员账户     彩金名称     彩金金额   备注   创建人   更新人  操作
# onwer_id     user_id     caijin_id

# 彩金添加
class MemberCaiJin(Base):
    __tablename__ = 'admin_member_caijin'
    id          = Column(Integer,      comment='ID', unique=True, primary_key=True, )
    member_id   = Column(Integer, ForeignKey("admin_member.id", ondelete='CASCADE', onupdate='CASCADE'))
    members     = relationship("Member", back_populates="caijins", lazy='joined',  passive_deletes=True)
    source_id   = Column(Integer, ForeignKey("admin_member_caijin_source.id", ondelete='CASCADE', onupdate='CASCADE'))
    sources     = relationship("MemberCaiJinSource", back_populates="sources", lazy='joined',  passive_deletes=True)
    money       = Column(DECIMAL(24,2), comment="彩金金额")
    description = Column(String(255),  comment='备注', index=True)
    first_name  = Column(String(255),  comment='创建者')
    last_name   = Column(String(255),  comment='最后一次更新者')
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))

    
    # source_id   = Column(Integer, ForeignKey("admin_member_caijin_source.id", ondelete='CASCADE', onupdate='CASCADE'))



# # 彩金添加来源
class MemberCaiJinSource(Base):
    __tablename__ = 'admin_member_caijin_source'
    id          = Column(Integer,      comment='ID', unique=True, primary_key=True, )
    name        = Column(String(255),  comment='标签名称', index=True, unique=True)
    color       = Column(String(255),  comment='标签颜色')
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))
    sources     = relationship("MemberCaiJin", back_populates="sources", lazy='dynamic',  passive_deletes=True)




# 会员信息库
class MemberProfile(Base):
    __tablename__ = 'admin_member_profile'
    id          = Column(Integer,      comment='ID', unique=True, primary_key=True)
    code        = Column(String(255),  comment='渠道号', index=True)
    account     = Column(String(255),  comment='会员账号', index=True)
    account_id  = Column(String(255),  comment='游戏ID', index=True)
    realname    = Column(String(255),  comment='真实姓名', index=True)
    contact     = Column(String(255),  comment='所属银行', index=True)
    iphone_num  = Column(String(255),  comment='电话号码', index=True)
    bank_number = Column(String(255),  comment='银行卡', index=True)
    description = Column(String(255),  comment='备注', index=True)
    first_name  = Column(String(255),  comment='创建者')
    last_name   = Column(String(255),  comment='更新者')
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))

    owner_id    = Column(Integer, ForeignKey("admin_group.id", ondelete='CASCADE', onupdate='CASCADE'))
    owner       = relationship("Group", back_populates="profiles", lazy='joined', passive_deletes=True)
    tags        = relationship('Tag',  secondary=admin_member_profile_tag,   back_populates="profiles", lazy='joined',   passive_deletes=True)




class IphoneNumber(Base):
    __tablename__ = 'admin_iphone_number'
    id          = Column(Integer,  comment='ID', unique=True, primary_key=True)
    number      = Column(String(255),  comment='手机号码', index=True, unique=True)
    first_name  = Column(String(255),  comment='创建者')
    last_name   = Column(String(255),  comment='更新者')
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))



'''                                        站点汇总                                 '''
# 站点标签

admin_website_tag = Table(
    "admin_website_tag",
    Base.metadata,
    Column("website_id",  Integer, ForeignKey("admin_website.id"), comment='站点ID'),  # 属性 外键
    Column("webtag_id", Integer, ForeignKey("admin_webtag.id"),    comment='标签ID'),  # 属性 外键
)


class WebTag(Base):
    __tablename__ = 'admin_webtag'
    id          = Column(Integer,      comment='ID', unique=True, primary_key=True, )
    name        = Column(String(255),  comment='标签名称', index=True, unique=True)
    color       = Column(String(255),  comment='标签颜色')
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))
    websites     = relationship('WebSite',  secondary=admin_website_tag,   back_populates="tags", lazy='dynamic', passive_deletes=True)



# 站点资料
class WebSite(Base):
    __tablename__ = 'admin_website'
    id             = Column(Integer,      comment='ID', unique=True, primary_key=True, )
    name           = Column(String(255),  comment='站点主域', index=True)
    child          = Column(Text(),  comment='站点子域')
    channel_code   = Column(String(255),  comment='渠道号', index=True)
    contact        = Column(String(255),  comment='站点联系方式', index=True)
    op_link        = Column(String(255),  comment='OP链接', index=True)
    parent_id      = Column(Integer, default=0, comment='父站点ID', index=True)
    wallet_address = Column(String(255), comment='钱包地址', index=True)
    description = Column(String(255),  comment='备注', index=True)
    gg_position = Column(String(255),  comment='广告位置', index=True)
    gg_price    = Column(String(255),  comment='广告价格', index=True)
    gg_time     = Column(String(255), comment='广告到期')
    gg_effect   = Column(String(255),  comment='广告效果', index=True)
    is_del      = Column(Integer, default=0, comment='是否已删除', index=True)
    first_name  = Column(String(255),  comment='创建者')
    last_name   = Column(String(255),  comment='最后一次更新者')
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))
    delete_at   = Column(TIMESTAMP(timezone=True))
    owner_id    = Column(Integer, ForeignKey("admin_group.id", ondelete='CASCADE', onupdate='CASCADE'))
    owner       = relationship("Group", back_populates="websites", lazy='joined', order_by='Group.id', passive_deletes=True)
    tags        = relationship('WebTag',  secondary=admin_website_tag,   back_populates="websites", lazy='joined',  order_by='WebTag.id', passive_deletes=True)
    



'''                                        关键词                                 '''

class keyWord(Base):
    __tablename__  = 'admin_keyword'
    id             = Column(Integer,      comment='ID', unique=True, primary_key=True)
    name           = Column(String(255),  comment='关键词名称', index=True)
    type           = Column(String(255),  comment='关键词类型', index=True)
    status         = Column(Integer,  comment='关键词状态', default=-2, index=True) # -2 未搜索， 1 已搜索， -1 正在搜素
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))
    search_user = Column(String(255),  comment='分配者')
    first_name  = Column(String(255),  comment='创建者')
    last_name   = Column(String(255),  comment='更新者')
    searchkeywords = relationship("searchKeyWord", back_populates="owner", lazy='joined', order_by='searchKeyWord.id')

class searchKeyWord(Base):
    __tablename__ = 'admin_searchkeyword'
    id            = Column(Integer,      comment='ID', unique=True, primary_key=True)
    number        = Column(Integer,  comment='排名序号', index=True)
    link          = Column(Text(),  comment='对应链接')
    url_website   = Column(String(255),  comment='网站网址', index=True)
    contact       = Column(String(255),  comment='联系方式', index=True)
    is_contact    = Column(Integer,  comment='是否锁定', default=0, index=True)
    contact_user  = Column(String(255),  comment='联系人', index=True)
    color         = Column(String(255),  comment='颜色', index=True)
    cn            = Column(String(255),  comment='中文')
    en            = Column(String(255),  comment='英文')
    owner_id      = Column(Integer, ForeignKey("admin_keyword.id", ondelete='CASCADE', onupdate='CASCADE'))
    owner         = relationship("keyWord", back_populates="searchkeywords", lazy='joined', order_by='keyWord.id', passive_deletes=True)
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))
    first_name  = Column(String(255),  comment='创建者')
    last_name   = Column(String(255),  comment='更新者')
    description = Column(String(255),   comment='描述')
    type        = Column(String(255),  comment='关键词类型', index=True)



class countSearchKeyWord(Base):
    __tablename__ = 'admin_count_searchkeyword'
    id            = Column(Integer, comment='ID', unique=True, primary_key=True)
    count_number  = Column(Integer, comment='统计序号', default=0, index=True)
    count_total   = Column(Integer, comment='总数量', default=0)
    count_sex     = Column(Integer, comment='SEX数量', default=0, index=True)
    count_other   = Column(Integer, comment='其他数量', default=0, index=True)
    count_wrong   = Column(Integer, comment='黄色数量', default=0, index=True)
    count_user    = Column(Integer, comment='统计用户', index=True)
    count_at      = Column(String(255),  comment='统计时间',index=True)









    '''                                        权重域名                                 '''

class Weight(Base):
    __tablename__  = 'admin_weight'
    id             = Column(Integer,      comment='ID', unique=True, primary_key=True)
    type           = Column(String(255),  comment='权重类别')
    name           = Column(Text(),  comment='权重名称')
    status         = Column(Integer,  comment='权重状态', default=-2, index=True) # -2 未搜索， 1 已搜索， -1 正在搜素
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))
    search_user = Column(String(255),  comment='分配者')
    first_name  = Column(String(255),  comment='创建者')
    last_name   = Column(String(255),  comment='更新者')
    searchweights = relationship("SearchWeight", back_populates="owner", lazy='joined', order_by='SearchWeight.id')

class SearchWeight(Base):
    __tablename__ = 'admin_searchweight'
    id            = Column(Integer,      comment='ID', unique=True, primary_key=True)
    number        = Column(Integer,  comment='排名序号', index=True)
    link          = Column(Text(),  comment='对应链接')
    url_website   = Column(Text(),  comment='网站网址')
    contact       = Column(String(255),  comment='联系方式', index=True)
    is_contact    = Column(Integer,  comment='是否锁定', default=0, index=True)
    contact_user  = Column(String(255),  comment='联系人', index=True)
    color         = Column(String(255),  comment='颜色', index=True)
    cn            = Column(String(255),  comment='中文')
    en            = Column(String(255),  comment='英文')
    owner_id      = Column(Integer, ForeignKey("admin_weight.id", ondelete='CASCADE', onupdate='CASCADE'))
    owner         = relationship("Weight", back_populates="searchweights", lazy='joined', order_by='Weight.id', passive_deletes=True)
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))
    first_name  = Column(String(255),  comment='创建者')
    last_name   = Column(String(255),  comment='更新者')
    description = Column(String(255),   comment='描述')



class CountSearchWeight(Base):
    __tablename__ = 'admin_count_searchWeight'
    id            = Column(Integer, comment='ID', unique=True, primary_key=True)
    count_number  = Column(Integer, comment='统计序号', default=0, index=True)
    count_total   = Column(Integer, comment='总数量', default=0)
    count_sex     = Column(Integer, comment='SEX数量', default=0, index=True)
    count_other   = Column(Integer, comment='其他数量', default=0, index=True)
    count_wrong   = Column(Integer, comment='黄色数量', default=0, index=True)
    count_user    = Column(Integer, comment='统计用户', index=True)
    count_at      = Column(String(255),  comment='统计时间',index=True)










# 任务记录
class taskRecord(Base):
    __tablename__ = 'admin_task'
    id            = Column(Integer, comment='ID', unique=True, primary_key=True)
    path          = Column(String(255),  comment='任务路径',index=True)
    task_name     = Column(String(255),  comment='任务名称',index=True)
    description   = Column(Text(),  comment='任务记录')
    progress      = Column(String(255),  comment='任务进度')
    first_name    = Column(String(255),  comment='任务人',index=True)
    created_at  = Column(TIMESTAMP(timezone=True),  server_default=text("now()"))
    updated_at  = Column(TIMESTAMP(timezone=True))










    '''                                        出款记录                                 '''
    # 盘口  会员ID  会员姓名  所属银行  支行  银行卡号  出款金额  提交时间  操作时间   提交人  二次确认  出款人  备注   截图

from enum import Enum,unique
@unique
class ReceState(Enum):
    wait  = 0  # 等待接单
    rece  = 1  # 已接单
    done  = 2  # 已完成
    error = 3  # 订单错误

class RecordOutMoney(Base):
    __tablename__ = 'admin_record_outmoney'
    id            = Column(Integer,      comment='ID', unique=True, primary_key=True)
    owner_id      = Column(Integer, ForeignKey("admin_group.id", ondelete='CASCADE', onupdate='CASCADE'), comment="归属部门")
    owner         = relationship("Group", back_populates="outmoneys", lazy='joined',  passive_deletes=True)
    uid           = Column(String(255),  comment='会员ID', index=True)
    bank_name     = Column(String(255),  comment='会员姓名',index=True)
    bank_owner    = Column(String(255),  comment='所属银行')
    bank_child    = Column(String(255),  comment='支行')
    bank_card     = Column(String(255),  comment='银行卡号',index=True)
    out_money     = Column(DECIMAL(24,2),comment='出款金额',index=True)
    first_name    = Column(String(255),  comment='提交员', index=True)
    last_name     = Column(String(255),  comment='接单员', index=True)
    two_enter     = Column(Integer,      comment='二次确认', default=0, index=True)
    rece_state    = Column(Integer,      comment='接单状态', index=True)
    description   = Column(Text(),       comment='备注')
    img_path      = Column(Text(),       comment='截图')
    created_at    = Column(TIMESTAMP(timezone=True),  server_default=text("now()"), comment='提交时间')
    updated_at    = Column(TIMESTAMP(timezone=True), comment='操作时间')
    

