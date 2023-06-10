from api.services import Crud
from api.utils import get_today
from api.models import WebSite,Group,WebTag
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy import or_,and_
from sqlalchemy.sql import text
# class MemberObj:



class Services:

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



    async def get_list(self, current_user, db, model, params=None, tab=None, field=None, order_by=None):
        if field and order_by:
            order_field = await self.get_order_field(model, field, order_by)
        else:
            order_field = []
        

        current_user_group_ids = list(map(lambda x:x.id, current_user.groups))

        filters = []
        
        # 是否搜索的是标签
        _tags = getattr(params, '_tags', None)
        if _tags:
            filters.append(model.tags)
            filters.append(WebTag.id.in_(_tags))


        # print(jsonable_encoder(params))
        # print(params.keywordType)
        # if params.keywordType:
        #     filters.append(text(f'''{params.keywordType} like {params.keyword}'''))

        _keywordType = getattr(params, 'keywordType', None)
        if _keywordType and _keywordType != 'all' and params.keyword:
            # 主域和子域同事搜索
            if _keywordType == 'name': 
                filters.append(or_(
                    model.name.like('%' + params.keyword + '%'),
                    model.child.like('%' + params.keyword + '%'),
                ))
            else:
                filters.append(text(f'''{params.keywordType} like "%{params.keyword}%"''')) 

        # 全局模糊搜索
        elif params.keyword:
            filters.append(or_(
                model.name.like('%' + params.keyword+ '%'),
                model.contact.like('%' + params.keyword+ '%'),
                model.wallet_address.like('%' + params.keyword+ '%'),
                model.description.like('%' + params.keyword+ '%'),
                model.child.like('%' + params.keyword+ '%'),
                model.channel_code.like('%' + params.keyword+ '%'),
                model.gg_effect.like('%' + params.keyword+ '%'),
                model.gg_position.like('%' + params.keyword+ '%'),
                model.op_link.like('%' + params.keyword+ '%'),
            ))
        else:
            pass


        if current_user.is_super:
            # 如果是超级管理员,获取所有数据，如果存在搜索关键词，则搜索关键词
            # query, total = await Crud.get_items(model=model, db=db,    params=params, other_filter=filters)

            if order_field:
                query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters, order_enable=True, order_field=order_field)
            else:
                query, total = await Crud.get_items(model=model, db=db,  params=params, other_filter=filters)
        else:
             # 如果不是超级管理员,模糊搜索可以搜索全局
            if params.keyword:
                # query, total = await Crud.get_items(model=model, db=db, params=params,  other_filter=filters)

                if order_field:
                    query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters, order_enable=True, order_field=order_field)
                else:
                    query, total = await Crud.get_items(model=model, db=db, params=params,  other_filter=filters)
            else:
                # 如果过滤的话，只能搜索用户本部门的数据
                filters.append(model.owner_id.in_(current_user_group_ids))
                # query, total = await Crud.get_items(model=model, db=db, params=params,  other_filter=filters)

                if order_field:
                    query, total = await Crud.get_items(model=model, db=db,  params=params,  other_filter=filters, order_enable=True, order_field=self.order_field)
                else:
                    query, total = await Crud.get_items(model=model, db=db, params=params,  other_filter=filters)

        
        # 关联 tag id
        for i in query:
            i.tag_id = [  r.id for r in i.tags ]

        # 如果超级管理员获取所有部门,否则只获取用户所属部门
        if current_user.is_super:
            _list = jsonable_encoder(query)
            g_query, _ = await Crud.get_items(db=db,model=Group, paging=False) 
        else:
            _list = jsonable_encoder(query) 
            g_query = current_user.groups

        for q in _list:
            if q['child']:
                q['child'] = q['child'].replace(',','\n')
            else:
                q['child'] = ''
                

        # 获取所有标签
        t_query, _ = await Crud.get_items(db=db,model=WebTag, paging=False)

        
        # 关键词可以搜索的字段
        keyWordSearchField = [
                {'label': '全局搜索', 'value': 'all'},
                {'label': '渠道号', 'value': 'channel_code'},
                {'label': '站点域名(包含子域)', 'value': 'name'},
                {'label': '联系方式', 'value': 'contact'},
                {'label': '钱包地址', 'value': 'wallet_address'},
            ]


        # 设置可以批量搜索的字段
        batchSearchField = [
                {'label': '渠道号', 'value': 'channel_code'},
                {'label': '站点域名(包含子域)', 'value': 'name'},
                {'label': '联系方式', 'value': 'contact'},
                {'label': '钱包地址', 'value': 'wallet_address'},
            ]

        # 设置可以批量更新的字段        
        batchModifyField = [
            {'label': '备注', 'value': 'description'},
            {'label': '标签', 'value': 'tag_id'},
            {'label': '钱包地址', 'value': 'wallet_address'},
            {'label': '联系方式', 'value': 'contact'},
            {'label': '广告位置', 'value': 'gg_position'},
            {'label': '广告价格', 'value': 'gg_price'},
            {'label': '广告到期，-> 时间格式例如: 1970-01-01 或者 1970/02/28', 'value': 'gg_time'},
            {'label': '广告效果', 'value': 'gg_effect'},
            {'label': 'OP链接', 'value': 'op_link'},
        ]

        batchSearchType = [
            {'label': '只包含正常数据', 'value': 0},
            {'label': '只包含删除数据', 'value': 1},
            {'label': '包含所有数据',   'value': 2},
        ]



        
        _total = total
        data = {
            'list': _list,
            'totalCount': _total,
            'groups': jsonable_encoder(g_query, include=['id', 'name']),
            'tags': jsonable_encoder(t_query),
            'keyWordSearchField': keyWordSearchField,
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

        filters.append(WebSite.channel_code.in_(key))
        filters.append(WebSite.owner_id==params.owner_id)

        # 获取用户归属组，只允许修改用户的组,管理员除外
        if not current_user.is_super:
            userGroups = [ g.id for g in current_user.groups]
            if params.owner_id not in userGroups:
                raise HTTPException(status_code=403, detail='不允许修改其他部门的数据')

        # 正常？ 回收站？ 全部
        if params.includeDelete != 2: # 2 代表全部
            filters.append(WebSite.is_del==params.includeDelete)


        

        data, _ = await Crud.get_items(db=db, model=WebSite, paging=False, other_filter=filters)

        if not data:
            raise HTTPException(status_code=400, detail='未搜索到需要更新的数据')

        # 如果更新的是标签
        

        
        # 替换数据
        for b in batchContent:
            for o in data:
                if params.tag_id:
                    tags = db.query(WebTag).filter(WebTag.id.in_(params.tag_id)).all() if params.tag_id else [], # 获取id obj
                    setattr(o, 'tags', tags[0])
                    continue
                if o.channel_code == b.get('code', '').replace(' ',''):   # 如果值相等
                    setattr(o, batchType, b['value'])
        db.commit()


    async def import_excel(self, current_user, params, db):


        data = params.importData

        '''------------------- 1、查询 归属系列是否存在有权限，如果不存在或者没权限，则返回错误 -----------------------------'''

        #  获取需要修改数据的归属部门
        owner = list(set(map(lambda x:x.get('owner', '').replace(" ", ''), data)))       # 归属系列


        #  如果不是超级用户
        if not current_user.is_super:
            # 获取当前用户所属组
            userGroups = [ g.name for g in current_user.groups]

            xo = list(set(owner).difference(set(userGroups)))    # owner 有，userGroups 没有

            # 判断如果数据不是用户所属组，不允许批量上传
            if len(xo) > 0:
                raise HTTPException(status_code=403, detail='不允许添加其他归属系列：{0}'.format(",".join(xo)))

        else:
            g_query, _ = await Crud.get_items(db=db, model=Group, paging=False) 
            allGroups = list(set(map(lambda x:x.name, g_query)))
            xo = list(set(owner).difference(set(allGroups)))

            if len(xo) > 0:
                raise HTTPException(status_code=403, detail='请先添加归属系列：{0}'.format(",".join(xo)))

        '''---------------------------------------------------------------------------------------------------------'''
        

        '''--------------------2、查询 当前用户部门系列下的渠道号的是否存在，如果不存在，则返回错误------------------------------------------------'''

        # 获取用户所有组，和组下所有渠道号,超级管理员获取所有
        # groupAndCode = {}
        # if not current_user.is_super:
        #     userGroups = [ g.id for g in current_user.groups]
        #     query,_ = await Crud.get_items(db=db, model=WebSite, paging=False, other_filter=[WebSite.owner_id.in_(userGroups), WebSite.is_del==0]) 
        # else:
        #     query,_ = await Crud.get_items(db=db, model=WebSite, paging=False, other_filter=[WebSite.is_del==0]) 
        
        # for o in owner:          # 循环文件内系列
        #     groupAndCode[o] = [] # 定义归属系列下数组
        #     for d in query:       # 循环数据库内系列
        #         if d.owner.name == o:
        #             groupAndCode[o].append(d.channel_code)

        # 比较文件上传内数据和数据库内数据， 如果文件内归属系列中的渠道号在数据中不存在，那么则返回错误
        # error_code = []
        # for f in data:
        #     # print(f'数据库中:', groupAndCode[f['owner']], '传输过来的:',f['channel_code']  )
        #     if str(f['channel_code']) not in groupAndCode[f['owner']]:
        #         error_code.append(f['channel_code'])
        
        
        # if error_code:
        #     raise HTTPException(status_code=403, detail='你所拥有的归属系列中没有此渠道号: {0}'.format(','.join(map(lambda x:str(x), error_code))))               
        '''---------------------------------------------------------------------------------------------------------'''

        '''--------------------2、查询 标签是否存在,子域不需要标签------------------------------------------------------------------'''

        excel_tags = list(set(filter(None,map(lambda x : x.get('tags', None), data))))       # 归属系列
        if excel_tags:
            t_query, _ = await  Crud.get_items(db=db, model=WebTag, paging=False, other_filter=[WebTag.name.in_(excel_tags)]) 
            db_exists = map(lambda x:x.name, t_query)
            xo = list(set(excel_tags).difference(set(db_exists)))
            if len(xo) > 0:
                raise HTTPException(status_code=400, detail='标签不存在：{0}'.format(','.join(xo)))


        # 获取所有标签
        # all_tags,_ = await Crud.get_items(db=db, model=WebTag, paging=False) 

        '''---------------------------------------------------------------------------------------------------------'''


        '''--------------------2、区分是添加数据, 还是更新数据-------------------------------------------------------'''
        # 获取组 id ，并组合
        _input_groupIds,_ = await Crud.get_items(db=db, model=Group, paging=False)
        _input_groupList = {}
        for i in _input_groupIds:
            _input_groupList.update({i.name:i.id})

        '''---------------------------------------------------------------------------------------------------------'''
        # 最后批量修改，并一次性提交

        for d in data:
            # m_query,_ = await Crud.get_items(db=db, model=WebSite, paging=False, other_filter=[WebSite.channel_code==d.get('channel_code', ''), WebSite.is_del==0])
            filters = [
                and_(
                    WebSite.is_del==0,
                    WebSite.owner_id==_input_groupList.get(d.get('owner', '').replace(" ",''), ''),
                    WebSite.channel_code==d.get('channel_code','').replace(" ",''),
                )
            ]

            m_query,_ = await Crud.get_items(db=db, model=WebSite, paging=False, other_filter=filters)

  

            if m_query:
                # 如果存在则更新，不存在则添加
                name = d.get('name', '').replace(" ",'')
                if m_query[0].child:
                    child = ','.join(list(set(m_query[0].child.split(',') + d.get('child',[]))))
                else:
                    child = ','.join(d.get('child',''))

                last_name = current_user.username
                description = d.get('description', '')
                tags = d.get('tags', None)
                updated_at = get_today(True)
                k = m_query[0]
                
                _spli = k.name + "," + str(name)
                name = ','.join(list(set(_spli.split(','))))

                k.name = name
                k.child = child
                k.description = description
                k.last_name = last_name
                k.updated_at = updated_at
                k.tags = k.tags + db.query(WebTag).filter(WebTag.name==tags).all() if tags else k.tags + []
                # setattr(k, 'name', name)
                # setattr(k, 'child', child)
                # setattr(k, 'last_name', last_name)
                # setattr(k, 'description', description)
                # setattr(k, 'updated_at', updated_at)   
            else:
                #如果不存在则添加
                owner_id = _input_groupList.get(d.get('owner', '').replace(" ",''), '')
                name =  d.get('name', '').replace(" ",'')
                child = ','.join(d.get('child',''))
                channel_code = d.get('channel_code','').replace(" ",'')
                description = d.get('description', '')

                # print(d.get('tags'))
                
                query = await Crud.create_item(
                        db=db, 
                        model=WebSite, 
                        name=name, 
                        child=child,
                        channel_code=channel_code,
                        parent_id=0,
                        description=description,
                        first_name=current_user.username,
                        tags = db.query(WebTag).filter(WebTag.name==d.get('tags')).all() if d.get('tags', None) else [],
                        owner_id=owner_id,
                )
                db.add(query)
        db.commit()        
            # 判断归属系列, 渠道编号是否相同, 如果相同则更新子数据和主域
            # for m in m_query:
            #     if m.owner.name == d.get('owner','') and m.channel_code == d.get('channel_code', ''): 
            #         m.name = d.get('name', '')
            #         m.child = m.child + ',{0}'.format(','.join(d.get('child',[])))
            #         continue
        

        


        # # 检测当前部门下是否已经存在了会员账号
        # import_user = list(map(lambda x:x.get('username',None), data))
        # is_exists, _ = await Crud.get_items(db=db, model=Member, paging=False, other_filter=[Member.username.in_(import_user), Member.owner_id==id])
        # if is_exists:
        #     _e = list(set(map(lambda x:x.username, is_exists)))
        #     raise HTTPException(status_code=400, detail=f'已存在VIP: {_e}')



        # # 组合成数据库想要的数据
        # newData = []
        # if not current_user.is_super:
        #     for d in data:
        #         newData.append({
        #                 'username': d.get('username', None), 
        #                 'realname': d.get('realname', None), 
        #                 'owner_id': id, 
        #                 'first_name': current_user.username 
        #             })
        # else:
        #     for d in data:
        #         newData.append({
        #                 'username': d.get('username', None), 
        #                 'realname': d.get('realname', None), 
        #                 'id_number': d.get('realname', None),  
        #                 'iphone': d.get('iphone',None),
        #                 'bank': d.get('bank', None), 
        #                 'owner_id': id, 
        #                 'first_name': current_user.username 
        #             })

        # try:
        #     db.execute(
        #         Member.__table__.insert(),
        #         newData
        #     )
        #     db.commit()
        # except Exception as e:
        #     from api.utils.logs import logger
        #     logger.error(str(e))
        #     raise HTTPException(status_code=400, detail='批量导入失败')

WebSiteServices = Services()

