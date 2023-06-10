from api.exts.init_database import SessionLocal
from api.services import Crud
from api.models import Member,Group,Tag
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy.sql import or_,and_
from api.utils import get_today

# class MemberObj:



class MemberObj:

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



        # for k,v in keyword.items():
        #     _is_exists = getattr(Member, k, None)
        #     if _is_exists and v:
        #         if v.lower() == 'desc':
        #             self.order_field.append(_is_exists.desc())
        #         elif v.lower() == 'asc':
        #             self.order_field.append(_is_exists.asc())
        #         else:
        #             pass
                # self.order_field.append(text(f'{}.{_is_exists} {v}'))


    async def get_list(self, current_user, db, model, params=None, tab=None, field=None, order_by=None):
        
        if field and order_by:
            order_field = await self.get_order_field(model, field, order_by)
        else:
            order_field = []
        

        # current_user_group_ids = list(map(lambda x:x.id, current_user.groups))

        filters = []
        # 是否搜索的是关键词
        _k = getattr(params, 'keyword', None)
        if _k:
            filters.append(or_(
                model.username.like("%" + _k + "%"),
                model.channel_code.like("%" + _k + "%"),
                model.register_ip.like("%" + _k + "%"),
                model.last_login_ip.like("%" + _k + "%"),
            ))
        
        # 是否搜索的是标签
        _tags = getattr(params, '_tags', None)
        if _tags:
            filters.append(model.tags)
            filters.append(Tag.id.in_(_tags))

        '''-----------------------------------------------------------------------------------'''
        # 排序


        '''-----------------------------------------------------------------------------------'''

        # if current_user.is_super:
        #     # 如果是超级管理员,获取所有数据，如果存在搜索关键词，则搜索关键词
        #     query, total = await Crud.get_items(model=Member, db=db,  params=params, other_filter=filters, order_enable=True, order_field=self.order_field)

        # else:
        #      # 如果不是超级管理员，则获取用户所关联部门相关的数据，搜索的时候搜索其他部门内容
        #     if params.keyword:
        #         query, total = await Crud.get_items(model=Member, db=db,  params=params,  other_filter=filters,order_enable=True, order_field=self.order_field)
        #     else:
        #         filters.append(Member.owner_id.in_(current_user_group_ids))
        if order_field:
            query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters, order_enable=True, order_field=order_field)
        else:
            query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters)
        # query, total = await Crud.get_items(model=Member, db=db,  params=params,  other_filter=filters)

        
        '''-----------------------------------------------------------------------------------'''
        # 关联 tag id, 添加新字段
        for i in query:
            i.tag_id = [  r.id for r in i.tags ]

        # 如果超级管理员获取所有部门,否则只获取用户所属部门，剔除手机和银行卡
        # if current_user.is_super:
        _list = jsonable_encoder(query)
        g_query, _ = await Crud.get_items(db=db,model=Group, paging=False) 
        # else:
        #     _list = jsonable_encoder(query) 
        #     g_query = current_user.groups

        # 获取所有标签
        t_query, _ = await Crud.get_items(db=db,model=Tag, paging=False)

        '''-----------------------------------------------------------------------------------'''
        
        # 设置超级管理员和普通用户可以搜索的字段
        batchSearchField = [
                {'label': '渠道号', 'value': 'channel_code'},
                {'label': '会员账号', 'value': 'username'},
            ]

        
        batchModifyField = [
            {'label': '备注', 'value': 'description'},
            {'label': '标签', 'value': 'tag_id'}
        ]

        batchSearchType = [
            {'label': '只包含正常数据', 'value': 0},
            {'label': '只包含删除数据', 'value': 1},
            {'label': '包含所有数据',   'value': 2},
        ]

        # if current_user.is_super:
        #     batchSearchField.append({'label': '银行卡', 'value': 'bank'})
        #     batchSearchField.append({'label': '手机号码', 'value': 'iphone'})
        #     batchSearchField.append({'label': '身份证号', 'value': 'id_number'})


        #     batchModifyField.append({'label': '银行卡', 'value': 'bank'})
        #     batchModifyField.append({'label': '手机号码', 'value': 'iphone'})
        #     batchModifyField.append({'label': '身份证号', 'value': 'id_number'})

        
        _total = total
        data = {
            'list': _list,
            'totalCount': _total,
            'groups': jsonable_encoder(g_query, include=['id', 'name']),
            'tags': jsonable_encoder(t_query,include=['id', 'name','color']),
            'batchSearchField': batchSearchField,
            'batchSearchType': batchSearchType,
            'batchModifyField': batchModifyField
            
        }

        # data['list'].sort(key=lambda x: x['id'], reverse=True)
        return data

    async def batch_modify(self, current_user, params, db):
        # {'batchType': 'username', 'batchContent': [{'a': 'b'}], 'includeDelete': 0}
        # 先获取类型数据对应的KEY，

        filters = []
        batchType = params.batchType
        batchContent = params.batchContent
        key = [ key['code'] for key in batchContent ]
        
        
        if len(batchContent) == 0:
            raise HTTPException(status_code=400, detail='请传入需要查询的内容')

        filters.append(Member.username.in_(key))
        filters.append(Member.owner_id==params.owner_id)

        # 获取用户归属组，只允许修改用户的组,管理员除外
        # if not current_user.is_super:
        #     userGroups = [ g.id for g in current_user.groups]
        #     if params.owner_id not in userGroups:
        #         raise HTTPException(status_code=403, detail='不允许修改其他部门的数据')

        # 正常？ 回收站？ 全部
        if params.includeDelete != 2: # 2 代表全部
            filters.append(Member.is_del==params.includeDelete)


        

        data, _ = await Crud.get_items(db=db, model=Member, paging=False, other_filter=filters)

        if not data:
            raise HTTPException(status_code=400, detail='未搜索到需要更新的数据')

        # 如果更新的是标签
        
            

        # 替换数据
        for b in batchContent:
            for o in data:
                # 北京时间
                o.last_name = current_user.username
                o.updated_at = get_today(hms=True)
                if params.tag_id:
                    tags = db.query(Tag).filter(Tag.id.in_(params.tag_id)).all() if params.tag_id else [], # 获取id obj
                    # print(type(tags[0]))
                    setattr(o, 'tags', tags[0])
                    continue
                if o.username == b.get('code', '').replace(' ',''):   # 如果值相等
                    # print('相等数据库数据:', o.username)
                    setattr(o, batchType, b['value'])
        db.commit()


    async def import_excel(self, current_user, params, db):

        invalid_data = []
        data = params.importData

        
        # 获取数据库当中的组数据
        obj_group,_ = await Crud.get_items(db=db, model=Group, paging=False, params=False)
        group_list = list(map(lambda x:x.id, obj_group))

        # 获取数据中的所有组ID
        import_group = list(map(lambda x:x.get('owner', None), data))

    

        # 组合组和用户IDS组,为下一步判断组下会员账号是否存在做组合
        group_user_ids = {}
        for g in import_group:
            group_user_ids.update({ g: []})

        for d in data:
            o_id = d['owner']
            d['username'] = str(d['username']).replace(" ",'')
            group_user_ids[o_id].append(str(d['username']))


        # filter(lambda d:(group_user_ids[d['owner']].append(d['username'])), data)

        # 查询数据库不同部门的数据是否存在
        is_exists_orm = []
        exists_groupId_username = {}    # 临时存储已有的数据
        exists_groupId_no_username = {}    # 临时存储没有的数据
        for k, v in group_user_ids.items():
            # print('item',k)
            # print('item',type(k))

            exists_groupId_username[k] = []
            exists_groupId_no_username[k] = []
            if isinstance(k, int) and k in group_list:  # 判断 k 是否是部门 ID int 类型
                # exists_groupId_username.update({ k: ''})
                is_exists, _ = await Crud.get_items(db=db, model=Member, paging=False, other_filter=[and_(Member.username.in_(v), Member.owner_id==k)])
                if is_exists:
                    is_exists_orm = is_exists_orm + is_exists
                    _s = list(map(lambda x:x.username, is_exists)) 
                    exists_groupId_username[k] =  exists_groupId_username[k] + _s    # 获取 k id 部门已经存在的数据， 并临时存储
                    exists_groupId_no_username[k] = exists_groupId_no_username[k] + list(set(v).difference(_s)) 
                else:
                    # print('差集:',list(set(group_user_ids[k]).difference(exists_groupId_username[k])))
                    exists_groupId_no_username[k] = exists_groupId_no_username[k]  + list(set(group_user_ids[k]).difference(exists_groupId_username[k]))  # 并临床存储数据库中没有的数据
            else:
                invalid_data.append(k)



        # print(group_list)
        # print(group_user_ids)
        # print(is_exists_orm)
        # print(exists_groupId_username)
        # print(exists_groupId_no_username)
        # raise HTTPException(status_code=400, detail='请先删除已存在的数据')




        # # 获取所有标签
        tags,_ = await Crud.get_items(db=db, model=Tag, paging=False)


        # 组合成数据库想要的数据
        insert_newData = []

        insert_total = 0
        update_total = 0
        error_data = []
        for d in data:
            d['owner_id'] = d.pop('owner')

            # 标签不覆盖
            q_tags = []
            for t in d['tags']:
                for q in tags:
                    if q.id == t:
                        q_tags.append(q)



            

            _register_at   = str(d.get('register_at',''),)
            _last_login_at = str(d.get('last_login_at',''))


            try:
                from datetime import datetime , timedelta

                # UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
                UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

                utc_time1 = datetime.strptime(_register_at, UTC_FORMAT)
                local_date1 = utc_time1 + timedelta(hours=8)
                _register_at = datetime.strftime(local_date1 ,'%Y-%m-%d %H:%M:%S')

                utc_time2 = datetime.strptime(_last_login_at, UTC_FORMAT)
                local_date2 = utc_time2 + timedelta(hours=8)
                _last_login_at = datetime.strftime(local_date2 ,'%Y-%m-%d %H:%M:%S')


            except Exception as e:
                pass
            # print(_register_at)
            # print(_last_login_at)


            # 判断数据是否在 不存在的临时存储数据中，如果存在，则属于新数据
            if d['owner_id'] in exists_groupId_no_username and  str(d['username']) in exists_groupId_no_username[d['owner_id']]:

                # print('不存在数据', d['owner_id'], d['username'])

                insert_newData.append(
                        Member(
                        username=d['username'],
                        channel_code=d.get('channel_code',None),
                        description =d.get('description',None),
                        tags=q_tags,
                        owner_id=d['owner_id'],
                        total_in_money=d.get('total_in_money', 0),
                        total_out_money=d.get('total_out_money', 0),
                        total_before_two_in_money=d.get('total_before_two_in_money', 0),
                        total_before_two_throw_money=d.get('total_before_two_throw_money', 0),
                        total_before_two_out_money=d.get('total_before_two_out_money', 0),
                        total_before_two_wax_money=d.get('total_before_two_in_money', 0) - d.get('total_before_two_out_money', 0),
                        total_wax_money=d.get('total_in_money', 0) - d.get('total_out_money', 0),
                        register_at   = _register_at,
                        last_login_at = _last_login_at,
                        register_ip   = d.get('register_ip',0),
                        last_login_ip = d.get('last_login_ip',0),
                        first_name    = current_user.username
                    )
                )
                insert_total += 1
            # 如果存在于 已存在的临时存储中,则更新
            elif d['owner_id'] in exists_groupId_username and  str(d['username']) in exists_groupId_username[d['owner_id']]:
                for k in is_exists_orm:
                    # print('已存在数据', k.username, d['username'], k.owner_id, d['owner_id'])
                    if str(k.username) == str(d['username']) and k.owner_id == d['owner_id']:
                        k.description = f"{d.get('description')}" if d.get('description',None) else k.description
                        # k.tags = q_tags
                        k.total_in_money  = d.get('total_in_money', 0)
                        k.total_out_money = d.get('total_out_money', 0)
                        k.total_before_two_in_money    = d.get('total_before_two_in_money', 0)
                        k.total_before_two_throw_money = d.get('total_before_two_throw_money', 0)
                        k.total_before_two_out_money   = d.get('total_before_two_out_money', 0)
                        k.total_before_two_wax_money   = d.get('total_before_two_in_money', 0) - d.get('total_before_two_out_money', 0)
                        k.total_wax_money = d.get('total_in_money', 0) - d.get('total_out_money', 0)
                        k.register_at     = _register_at
                        k.last_login_at   = _last_login_at
                        k.register_ip     = d.get('register_ip',None)
                        k.last_login_ip   = d.get('last_login_ip',None)
                        k.last_name=current_user.username
                        k.updated_at = get_today(hms=True)

                        update_total += 1
            else:
                error_data.append(d)


        

        try:
            db.commit()
            # db.execute(
            #     Member.__table__.insert(),
            #     data
            # )
            # from sqlalchemy.orm import  Session

            # ORM 必须重新创建一个Seession,不然会出现二次提交，数据重复
            s = SessionLocal()
            s.bulk_save_objects(insert_newData)
            s.commit()

            return insert_total, update_total, error_data
        except Exception as e:
            from api.utils.logs import logger
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='批量导入失败')

memberServices = MemberObj()
