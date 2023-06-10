
from api.exts.init_database import SessionLocal
from api.services import Crud
from api.models import Member,Group,MemberCaiJinSource,MemberCaiJin,IphoneNumber,taskRecord
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy.sql import and_
from api.utils import get_progress


class Obj:

    def __init__(self) -> None:
        self.order_field = []

    async def get_order_field(self, model, field, order_by):
        self.order_field = []
        order_by_list = ['asc', 'desc']
        if order_by.lower() not in order_by_list:
            raise HTTPException(status_code=400, detail='排序方法错误,请使用 asc 或者 desc')

        _is_exists = getattr(model, field, None)
        if _is_exists:
            if order_by.lower() == 'desc':
                self.order_field.append(_is_exists.desc())
            else:
                self.order_field.append(_is_exists.asc())
        else:
            raise HTTPException(status_code=400, detail='无此方法排序')



    async def get_list(self, db, model, params):


        filters = []

        _keyword = getattr(params, 'keyword', None)
        _start_end = getattr(params, '_start_end', None)
        _update_start_end = getattr(params, '_update_start_end', None)
        _first_name = getattr(params, '_first_name', None)
        _last_name = getattr(params, '_last_name', None)

        # 是否搜索手机号码
        if _keyword:
            filters.append(model.number.like('%' + _keyword + '%'))

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

        if self.order_field:
            query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters, order_enable=True, order_field=self.order_field)
        else:
            query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters)

        return jsonable_encoder(query), total



    # async def excel_import(self, db, data, current_user):
    #     # {'importData': [{'owner': '运开测试', 'username': 111111, 'source': '生日彩金', 'money': 500, 'description': 123}]}
    #     # 1、先所有所有部门
    #     newData = []
    #     errData = []
    #     _groupDict = {}     # 数据库组名，id, 字典
    #     _groupUserDict = {}
    #     _userDict = {}      # 会员名字对应对应ID
    #     _sourceDict = {}    # 数据库彩金源 字典
    #     query_group,_  = await Crud.get_items(db=db, model=Group, paging=False)
    #     query_source,_ = await Crud.get_items(db=db, model=MemberCaiJinSource, paging=False)
        

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
    #         owner = d.get('owner',None)
    #         source = d.get('source',None)
    #         username = str(d.get('username', None))
    #         money = d.get('money',0)

    #         if owner and source and username and  owner in _groupDict and source  in _sourceDict and username in _groupUserDict[owner] and isinstance(money, int) or isinstance(money, float):
    #             # 如果存在则组合成数据库对应数据

    #             _c = {}
    #             _c['member_id']    = _userDict[f"{owner}_{username}"]
    #             _c['source_id']    = _sourceDict[source]
    #             _c['money']        = decimal.Decimal(money)
    #             _c['description']  = d.get('description',None)
    #             _c['first_name']   = current_user.username
    #             newData.append(_c)
    #         else:
    #             errData.append(d)


    #     # 插入数据库
    #     try:
    #         if newData:
    #             db.execute(
    #                 MemberCaiJin.__table__.insert(),
    #                 newData
    #             )
    #             db.commit()
    #         return newData, errData
    #     except Exception as e:
    #         from api.utils.logs import logger
    #         logger.error(str(e))
    #         raise HTTPException(status_code=400, detail='导入数据失败')


    @staticmethod
    def get_date(path, db, current_user, item):

        _insert_data = []
        _exists = []
        error_data = []
        _data = list(set(map(lambda x:x.get('number',None), item.importData)))
        _obj = db.query(IphoneNumber).filter(IphoneNumber.number.in_(_data)).all()
        if _obj:
            _obj_data = list(map(lambda x:int(x.number), _obj))
            _exists = _obj_data

            # 筛选出新加的数据
            _new_obj_data = list(set(_data).difference(set(_obj_data)))
            for p in _new_obj_data:
                _insert_data.append({ 'number': p })
        else:
            _insert_data = _insert_data + item.importData


        # insert_total, update_total, error_data = len(_insert_data), 0, 0



        try:
            path        = path
            task_name   ='手机号码批量导入'
            first_name  = current_user.username
            

            description = {
                        "insert": '',
                        'exists': '',
                        'error': '',
                        'insert_total': 0,
                        'exists_total': 0,
                        'error_total':0,
                    }

            if _insert_data:

                # 进度条设置
                for _i in _insert_data:
                    # import time
                    # time.sleep(1)

                
                    # 获取进度
                    progress = get_progress(_insert_data.index(_i), len(_insert_data))
                    
                    # 如果不是 100 %
                    is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.progress != '100')).first()
                    if is_exist:
                        is_exist.progress = progress
                    else:
                        # 反之保存任务到数据库
                        description['insert'] = _insert_data
                        description['exists'] = _exists
                        description['error'] = error_data
                        description['insert_total'] = len(_insert_data)
                        description['exists_total'] = len(_exists)
                        description['error_total'] = len(error_data)

                        _record = taskRecord(
                            path        = path,
                            task_name   = task_name,
                            progress    = progress,
                            description = str(description),
                            first_name  = first_name,

                        )
                        db.add(_record)


                    # 导入数据
                    number = _i.get('number',None)
                    if number:
                        _new = IphoneNumber(number=number, first_name=first_name)
                        db.add(_new)
                    db.commit()


                # 最后设置 100%
                t_is_exist= db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.progress != '100')).first()
                t_is_exist.progress = 100
                db.commit()
            else:


                description['insert'] = _insert_data
                description['exists'] = _exists
                description['error'] = error_data
                description['insert_total'] = len(_insert_data)
                description['exists_total'] = len(_exists)
                description['error_total'] = len(error_data)

                _record = taskRecord(
                            path        = path,
                            task_name   = task_name,
                            progress    = 100,
                            description = str(description),
                            first_name  = first_name,

                        )
                db.add(_record)
                db.commit()


                        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f'{str(e)}')


services = Obj()