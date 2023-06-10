
from api.exts.init_database import SessionLocal
from api.services import Crud
from api.models import Member,Group,MemberCaiJinSource,MemberCaiJin,taskRecord
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.sql import and_
import decimal
from api.utils import get_progress

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



    async def get_list(self, db, model, params, filters=[], field=None, order_by=None):

        if field and order_by:
            order_field = await self.get_order_field(model, field, order_by)
        else:
            order_field = []

        filters = filters

        _g = getattr(params, 'owner_id', None)
        _tags = getattr(params, '_tags', None)
        _start_end = getattr(params, '_start_end', None)
        _update_start_end = getattr(params, '_update_start_end', None)
        _first_name = getattr(params, '_first_name', None)
        _last_name = getattr(params, '_last_name', None)


        # 如果搜索所属部门
        if _g:
            filters.append(model.members)
            filters.append(Member.owner_id==_g)

        # 是否搜索的是标签
        if _tags:
            filters.append(model.sources)
            filters.append(MemberCaiJinSource.id.in_(_tags))

        # 是否搜索导入者
        if _first_name:
            filters.append(model.first_name==_first_name)


        # 是否搜索更新者
        if _last_name:
            filters.append(model.last_name==_last_name)

        #  是否搜索创建时间
        if _start_end:
            _start_end = _start_end.split(',')
            if len(_start_end) == 2:
                filters.append(model.created_at.between(_start_end[0], _start_end[1]))

        #  是否搜索更新时间
        if _update_start_end:
            _update_start_end = _update_start_end.split(',')
            if len(_update_start_end) == 2:
                filters.append(and_(model.updated_at.between(_update_start_end[0], _update_start_end[1]), model.updated_at != None))


        # _a = await Crud.show_item(db=db, model=model, id=_m)
        # print(_a)

        if order_field:
            query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters, order_enable=True, order_field=order_field)
        else:
            query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters)

        return jsonable_encoder(query), total


    # @staticmethod
    # def excel_import(path , db, current_user, item):
    #     # {'importData': [{'owner': '运开测试', 'username': 111111, 'source': '生日彩金', 'money': 500, 'description': 123}]}
    #     # 1、先所有所有部门
    #     data = item.importData

    #     newData = []
    #     errData = []
    #     _groupDict = {}     # 数据库组名，id, 字典
    #     _groupUserDict = {}
    #     _userDict = {}      # 会员名字对应对应ID
    #     _sourceDict = {}    # 数据库彩金源 字典
    #     query_group  = db.query(Group).all()
    #     query_source = db.query(MemberCaiJinSource).all()
        

    #     # 组
    #     for g in query_group:
    #         _groupDict.update({g.name: g.id})
    #         _username = g.members.all()
            
    #         if _username:
    #             _groupUserDict.update({g.name: list(map(lambda x:x['username'], jsonable_encoder(_username,include=['id',  'username'])))})
                
    #             for k in _username:
    #                 _userDict[f"{k.owner.name}_{k.username}"] = k.id
    #         else:
    #             _groupUserDict.update({g.name: []})

    #     # 彩金来源
    #     for s in query_source:
    #         _sourceDict.update({s.name: s.id})


        

    #     # 2、判断组、会员账号、彩金来源是否同时存在，如果不存在则临时存放  
    #     for d in data:
    #         owner = str(d.get('owner','')).replace(" ","")
    #         source = str(d.get('source','')).replace(" ","")
    #         username = str(d.get('username', '')).replace(" ","")
    #         money = str(d.get('money','')).replace(" ","")
        


    #         if owner and source and username and  owner in _groupDict and source  in _sourceDict and username in _groupUserDict[owner]:

    #             try:
                   
    #                 _c = {}
    #                 _c['member_id']    = _userDict[f"{owner}_{username}"]
    #                 _c['source_id']    = _sourceDict[source]
    #                 _c['money']        = decimal.Decimal(money)
    #                 _c['description']  = d.get('description',None)
    #                 _c['first_name']   = current_user.username
    #                 newData.append(_c)
    #             except:
    #                 errData.append(d)
    #         else:
    #             errData.append(d)

    #     # print(newData)
    #     # print(errData)


    #     # 插入数据库
    #     # try:

    #     path        = path

    #     description = {
    #                 "insert": '',
    #                 'exists': '',
    #                 'error': '',
    #                 'insert_total': 0,
    #                 'exists_total': 0,
    #                 'error_total':0,
    #             }

    #     # print(newData)
    #     if newData:
    #         # 进度条设置
    #         num = 1
    #         for _i in newData:
    #             description['insert'] = newData
    #             description['exists'] = 0
    #             description['error'] = errData
    #             description['insert_total'] = len(newData)
    #             description['exists_total'] = 0
    #             description['error_total'] = len(errData)

    #             # 获取进度
    #             progress = get_progress(num, len(newData))
    #             is_exist = db.query(taskRecord).order_by(taskRecord.id.desc()) .filter(and_(taskRecord.path==path, taskRecord.progress != '100')).first()
    #             is_exist.progress = progress
    #             is_exist.description = str(description)
    #             db.commit()
                

    #             # 导入数据
    #             if  _i['member_id'] and _i['source_id'] and _i['money']:
    #                 _new = MemberCaiJin(
    #                         member_id   = _i['member_id'] , 
    #                         source_id   = _i['source_id'],
    #                         money       = _i['money'],
    #                         description = _i['description'],
    #                         first_name  = current_user.username,
    #                     )

    #                 db.add(_new)
    #             db.commit()

    #             # 彩金数量相加
    #             _show = db.query(Member).filter(Member.id == _i['member_id']).first()
    #             if _show:
    #                 _show.total_caijin_money = _show.total_caijin_money + decimal.Decimal(_i['money'])
    #                 db.commit()

    #             # # 最后设置 100%
    #             # t_is_exist= db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.progress != '100')).first()
    #             # t_is_exist.progress = 100
    #             # db.commit()

                
    #             num += 1
    #     else:
    #         is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.progress != '100')).first()
    #         is_exist.progress = 100
    #         db.commit()
    #         # pass




        # except Exception as e:
        #     from api.utils.logs import logger
        #     logger.error(str(e))
        #     db.rollback()
        #     raise HTTPException(status_code=400, detail='导入数据失败')



    @staticmethod
    def watchCountCaiJin(db, model, newData: Optional[List] = []):
        # with open("log.txt", mode="w") as f:
        #     content = f"message is {newData}"
        #     f.write(content)

        try:
            for item in newData:
                _show = db.query(model).filter(model.id == item.get('member_id', -999999999999999999999)).first()
                if _show:
                    _show.total_caijin_money = _show.total_caijin_money + decimal.Decimal(item.get('money', 0))
            db.commit()
        except Exception as e:
            from api.utils.logs import logger
            logger.error(str(e))


services = Obj()