from api.exts.init_database import SessionLocal
from api.services import Crud
from api.models import Member,Group,Tag,User,MemberProfile,taskRecord
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy.sql import or_,and_
from api.utils import get_today
from api.utils import get_progress, get_today
from api.tasks.task_db_base import db

class Obj:

    # def __init__(self) -> None:
    #     self.order_field = []


    async def get_order_field(self, model, field, order_by):
        order_field = []
        order_by_list = ['asc', 'desc']
        if order_by.lower() not in order_by_list:
            raise HTTPException(status_code=400, detail='排序方法错误,请使用 asc 或者 desc')

        _is_exists = getattr(model, field, None)
        if _is_exists:
            if order_by.lower() == 'desc':
                order_field.append(_is_exists.desc())
            else:
                order_field.append(_is_exists.asc())
            return order_field
        else:
            raise HTTPException(status_code=400, detail='无此方法排序')



    async def asy_get_users(self, db, model):
        users,_ =  await Crud.get_items(db=db, model=model, paging=False)
        _users = list(map(lambda x:x.username, users))
        return _users

        


    async def get_list(self,  db, model, params=None, field=None, order_by=None):
        
        filters = []

        if field and order_by:
            order_field = await self.get_order_field(model, field, order_by)
        else:
            order_field = []


        # 是否搜索的是关键词
        _k = getattr(params, 'keyword', None)
        if _k:
            filters.append(or_(
                model.code.like("%" + _k + "%"),
                model.account.like("%" + _k + "%"),
                model.account_id.like("%" + _k + "%"),
                model.realname.like("%" + _k + "%"),
                model.iphone_num.like("%" + _k + "%"),
                model.bank_number.like("%" + _k + "%"),
                model.description.like("%" + _k + "%"),
            ))
        

        # 是否搜索的是标签
        _tags = getattr(params, '_tags', None)
        if _tags:
            filters.append(model.tags)
            filters.append(Tag.id.in_(_tags))


        # 搜索创建者
        _first_name = getattr(params, '_first_name', None)
        if _first_name:
            filters.append(model.first_name==_first_name)

        # 搜索更新者
        _last_name = getattr(params, '_last_name', None)
        if _last_name:
            filters.append(model.last_name==_last_name)

        # 是否排序
        if order_field:
            query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters, order_enable=True, order_field=order_field)
        else:
            query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters)


        # 关联 tag id, 添加新字段
        for i in query:
            i.tag_id = [  r.id for r in i.tags ]


        # 获取所有用户
        users = await self.asy_get_users(db=db, model=User)
        _total = total
        data = {
            'list': jsonable_encoder(query),
            'users': jsonable_encoder(users),
            'totalCount': _total,
        }


        return data



    # # 文件上传导入
    # @staticmethod
    # def import_excel(gid, path, current_user, data):

    #     query_tags      = db.query(Tag).all()

    #     if data:
    #         if len(data) > 20:
    #             setp = int(len(data) / 20)
    #         else:
    #             setp = 2

    #         # 进度条设置
    #         n = 0
    #         insert_total = 0
    #         update_total = 0
    #         error_total  = 0
    #         error        = []


    #         while n > -1:
    #             # 切片设置
    #             ds = data[n:n+setp]
    #             inset_data  = []
    #             update_data = []
    #             temp_update = {}



    #             if ds:
    #                 for d in ds:
    #                     owner   = str(d.get('owner','')).replace(" ","")
    #                     account = str(d.get('account','')).replace(" ","")
    #                     _tags   = str(d.get('tags', '').replace(" ",""))
    #                     tags    = []

    #                     for t in query_tags:
    #                         if t.name == _tags:
    #                             tags.append(t)

    #                     d['tags'] = tags


    #                 # 组合数据
    #                 _dsUser      = list(map(lambda x:x['account'], ds))
    #                 _isInDbQuery = db.query(MemberProfile).filter(and_(MemberProfile.owner_id==gid, MemberProfile.account.in_(_dsUser))).all()   # 从数据库查询数据
    #                 _isInDbList  = list(map(lambda x:x.account, _isInDbQuery))                                                 # 组合从数据库拿到的数据
    #                 # _noInDb      = list(set(_dsUser).difference(set(_isInDbList)))                                           # 筛选不存在的数据


    #                 for d in ds:
    #                     _owner   = d['owner']
    #                     _account = d['account']
    #                     _tags    = d['tags']

    #                     if _owner and _account and _account not in _isInDbList:
    #                         inset_data.append(
    #                                 MemberProfile(
    #                                     owner_id    = gid,
    #                                     code        = d.get('code',None),
    #                                     account     = account,
    #                                     account_id  = d.get('account_id',None),
    #                                     realname    = d.get('realname', None),
    #                                     iphone_num  = d.get('iphone_num', None),
    #                                     contact     = d.get('contact', None),
    #                                     bank_number = d.get('bank_number', None),
    #                                     tags        = _tags,
    #                                     description = d.get('description', None),
    #                                     first_name  = current_user.username,
    #                             )
    #                         )
                            
    #                         insert_total += 1 
    #                     elif _owner and _account and _account in _isInDbList:
    #                         update_data.append(d)
    #                         temp_update.update({_account: d})
    #                         update_total += 1
    #                     else:
    #                         error.append(_account)
    #                         error_total += 1

    #                 if update_data:
    #                     _isInDbUp = db.query(MemberProfile).filter(and_(MemberProfile.owner_id==gid, MemberProfile.account.in_(temp_update.keys()))).all()
    #                     for _isIn in _isInDbUp:
    #                         _isIn.code        = d.get('code',None)
    #                         _isIn.account_id  = d.get('account_id',None)
    #                         _isIn.realname    = d.get('realname', None)
    #                         _isIn.contact     = d.get('contact', None)
    #                         _isIn.bank_number = d.get('bank_number', None)
    #                         _isIn.tags        = d.get('tags', [])
    #                         _isIn.description = d.get('description', None)
    #                         _isIn.last_name   = current_user.username
    #                         _isIn.updated_at  = get_today(hms=True)

    #                     # 提交更新
    #                     try:
    #                         db.commit()
    #                     except Exception as e:
    #                         update_total = update_total - len(update_data)
    #                         error_total  = error_total + len(update_data)
    #                         for i in update_data:
    #                             error.append(i['account'])

    #                 # 提交插入
    #                 try:
                            
    #                     if inset_data:
    #                         db.execute(
    #                             MemberProfile.__table__.insert(),
    #                             inset_data
    #                         )
    #                     db.commit()
    #                 except Exception as e:
    #                     if inset_data:
    #                         for i in inset_data:
    #                             error.append(i['account'])

    #                         error_total = error_total + len(inset_data)
    #                         insert_total = insert_total - len(inset_data)
    #                     from api.utils.logs import logger
    #                     logger.error(str(e))


                
                    
    #                 # 获取进度
    #                 description = {
    #                     'error': error[:100],
    #                     'insert_total': insert_total,
    #                     'update_total': update_total,
    #                     'error_total': error_total,
    #                 }

    #                 progress = get_progress(n, len(data))
    #                 is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
    #                 is_exist.progress    = progress
    #                 is_exist.description = str(description)
    #                 is_exist.updated_at  = get_today(hms=True)
    #                 db.commit()

    #                 n += setp
                

    #             else:
    #                 is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
    #                 is_exist.progress = 100
    #                 is_exist.updated_at  = get_today(hms=True)
    #                 db.commit()
    #                 break




services = Obj()