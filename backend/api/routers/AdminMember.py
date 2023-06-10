from fastapi import APIRouter,Depends,Request,Query,HTTPException,BackgroundTasks
from fastapi.encoders import jsonable_encoder
from api.models import Member,Tag,taskRecord,Group
from api.schemas import CreateMemberSchema,multideleteMemberSchema,multiSearchMemberSchema,importDataSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud,LoginCrud,memberServices
from sqlalchemy.orm import Session 
from api.utils.response import Success
from typing import Optional
from sqlalchemy.sql import and_
from api.utils import logger,get_today
import decimal
from api.tasks import excel_import_member
from datetime import datetime, timedelta
from api.exts import Schedule
import uuid
from api.dependen.lockRedis import lock

import json





# 重写json序列化类,解决 `TypeError: Object of type 'datetime' is not JSON serializable`
class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, datetime.date):  
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj)


router = APIRouter()

# 批量搜索
@router.post("/member/search/multi")
@require_token('multiSearchMember,POST')
async def multi_get_member(request: Request, item: multiSearchMemberSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    filters = []
    batchType = item.batchType
    batchContent = item.batchContent



    if len(batchContent) == 0:
        raise HTTPException(status_code=400, detail='请传入需要查询的内容')


    _search_type = getattr(Member, batchType, None)
    if _search_type:
        filters.append(_search_type.in_(batchContent))
    else:
        raise HTTPException(status_code=400, detail='请传入规定可以搜索内容')



    if item.includeDelete != 2: # 2 代表全部
        filters.append(Member.is_del==item.includeDelete)


    # 部门
    if item.owner_id:
        filters.append(Member.owner_id==item.owner_id)
    '''------------------------------------------------'''

    data, _ = await Crud.get_items(db=db, model=Member, paging=False, other_filter=filters)


    # 关联 tag id 添加新字段
    for i in data:
        i.tag_id = [  r.id for r in i.tags ]

    return Success(data=jsonable_encoder(data))

# 批量修改
@router.post("/member/modify/multi")
@require_token('multiModifyMember,POST')
async def multi_modify_member(request: Request, item: multiSearchMemberSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    setattr(item, 'owner_id', item.owner_id)

    # 组成成数组
    if isinstance(item.batchContent, str):
        newbatchContent = []
        
        batchContent = item.batchContent.split('\n')
        for b in batchContent:
            if item.batchType != 'tag_id':
                newC = b.split(' ')
                # if len(newC) != 2:
                    # raise HTTPException(status_code=400, detail='格式不正确')
                newbatchContent.append({'code':newC[0], 'value': ','.join(newC[1:]) })
            else:
                newbatchContent.append({'code':b, 'value': ''})
            
        item.batchContent = newbatchContent
    
    await memberServices.batch_modify(db=db, params=item, current_user=current_user)

    return Success()

# 批量删除
@router.post("/member/multi")
@require_token('multideleteMember,POST')
async def multi_del_member(request: Request, item: multideleteMemberSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    # # 如果不是超级用户
    # if not current_user.is_super:
    #     # 获取当前用户所属组
    #     userGroups = [ g.id for g in current_user.groups]

    #     # 获取需要删除的 ids 对应的组
    #     ids_obj,_ = await Crud.get_items(model=Member, db=db, other_filter=[Member.id.in_(item.ids)])
    #     ids_groups = list(set(map(lambda x:x.owner_id, ids_obj)))

    #     # 通过差集的方式获取不同，判断如果数据不是用户所属组，不允许批量删除
    #     if list(set(ids_groups).difference(set(userGroups))):
    #         raise HTTPException(status_code=403, detail='不允许删除其他部门数据')
    # '''------------------------------------------------'''

    await Crud.multi_delete(db=db, model=Member, ids=item.ids, last_name=current_user.username)
    return Success()


# 批量回收
@router.post("/member/recover")
@require_token('multirecoverMember,POST')
async def multi_rec_member(request: Request, item: multideleteMemberSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    # 如果不是超级用户
    # if not current_user.is_super:
    #     # 获取当前用户所属组
    #     userGroups = [ g.id for g in current_user.groups]
        
    #     # 获取需要删除的 ids 对应的组
    #     ids_obj,_ = await Crud.get_items(model=Member, db=db, other_filter=[Member.id.in_(item.ids)])
    #     ids_groups = list(set(map(lambda x:x.owner_id, ids_obj)))

    #     # 通过差集的方式获取不同，判断如果数据不是用户所属组，不允许批量删除
    #     if list(set(ids_groups).difference(set(userGroups))):
    #         raise HTTPException(status_code=403, detail='不允许还原其他部门数据')
        
    '''------------------------------------------------'''

    await Crud.recover_delete(db=db, model=Member, ids=item.ids, last_name=current_user.username)
    return Success()


# 批量清空
@router.post("/member/clear")
@require_token('multiclearMember,POST')
async def multi_clear_member(request: Request, item: multideleteMemberSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    # 如果不是超级用户
    # if not current_user.is_super:
    #     # 获取当前用户所属组
    #     userGroups = [ g.id for g in current_user.groups]
        
    #     # 获取需要删除的 ids 对应的组
    #     ids_obj,_ = await Crud.get_items(model=Member, db=db, other_filter=[Member.id.in_(item.ids)])
    #     ids_groups = list(set(map(lambda x:x.owner_id, ids_obj)))

    #     # 通过差集的方式获取不同，判断如果数据不是用户所属组，不允许批量删除
    #     if list(set(ids_groups).difference(set(userGroups))):
    #         raise HTTPException(status_code=403, detail='不允许清空其他部门数据')
        
    '''------------------------------------------------'''

    await Crud.clear_delete(db=db, model=Member, ids=item.ids)
    return Success()



# 批量导入
@router.post("/member/batch/import")
@require_token('importExcelMember,POST')
@lock('excel_import_member')
async def import_excel_member(request: Request, item: importDataSchema,   background_task:BackgroundTasks, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    before_30_min = next_cmd = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    _path = request.scope['path']
    _uuid = uuid.uuid1().hex
    path = f'{_path}_{_uuid}'

    # 批量导入前 30 分钟查询是否存在有人提交了任务
    is_exist_task,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path.like(_path + "%"), taskRecord.progress != 100, taskRecord.created_at > before_30_min)])
    if is_exist_task:
        raise HTTPException(status_code=400, detail=f"{is_exist_task[0].created_at} {is_exist_task[0].first_name} 任务进度 {int(is_exist_task[0].progress)}% 正在运行中 , 请等任务完成后或者5分钟后再次提交")



    upload_group = list(set(map(lambda x:str(x.get('owner','')).replace(" ",""), item.importData)))
    if len(upload_group) > 1:
        raise HTTPException(status_code=400, detail='每次上传只允许上传一个部门数据')


    # 查询部门是否存在
    is_group,_ = await Crud.get_items(db=db, model=Group, other_filter=[Group.name==upload_group[0]])
    if not is_group:
        raise  HTTPException(status_code=400, detail='部门不存在')

    #


    # await Crud.create_item(db=db, model=taskRecord, path=path,  task_name='会员资料导入', progress=0, first_name=current_user.username)

    # excel_import_member(is_group[0].id, path, current_user.username, item.importData)
    # 当前时间的后 10 秒执行导入
    next_cmd = (datetime.now() + timedelta(seconds=5)).strftime("%Y-%m-%d %H:%M:%S")
    # next_cmd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Schedule.add_job(excel_import_member, 'date',  run_date=next_cmd, misfire_grace_time=3600, args=[is_group[0].id, path, current_user.username, item.importData])

    return Success(data={'task_id': path })


# 获取计划任务
@router.get("/member/batch/import")
@require_token('importExcelMember,POST')
async def batch_import_member(request: Request, task_id: str = Query(...),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # _path = request.scope['path']

    _rdata,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path==task_id, taskRecord.first_name==current_user.username)])
    if _rdata:
        return Success(data={ "task": jsonable_encoder(_rdata[0])})
    else:
        return Success(data={ "task": {'progress': 0}})



# 列
@router.get("/members/")
@require_token('getListMember,GET')
async def get_member_list(
        request: Request, 
        params: CommonQueryParams = Depends(), 
        tab: Optional[str] = Query(None), 
        owner_id: Optional[int] = Query(None),
        owner_tag_id: Optional[str] = Query(None), 
        current_user: LoginCrud.verify_token = Depends(), 
        db: Session = Depends(get_db),
        field: Optional[str] = Query(None),
        order_by: Optional[str] = Query(None),
    ):

    # 设置搜索部门
    if owner_id is not None:
        setattr(params, 'owner_id', owner_id) 

    # 标签搜索
    if bool(owner_tag_id):
        _tags = list(map(int, owner_tag_id.split(','))) or list[int(owner_tag_id)]
        setattr(params, '_tags', _tags) 
        # filters.append(Member.tag)
        # filters.append(Tag.id.in_(_tags))
    # tab 标签切换，搜索是否删除字段
    setattr(params, 'is_del', 0) if tab == 'all' else setattr(params, 'is_del', 1)
    
 
    # 获取排序
    # if field and order_by:
    #     await memberServices.get_order_field(
    #         model=Member,
    #         field=field,
    #         order_by=order_by,
    #     )

    # 返回总数据

    data = await memberServices.get_list(
            current_user=current_user,
            db=db, 
            model=Member,
            params=params, 
            tab=tab,
            field=field,
            order_by=order_by,
    )
    return Success(data=data)


# 查
@router.get("/member/{id}")
@require_token('getMember,GET')
async def get_member(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=Member, id=id)
    return Success(data=jsonable_encoder(query))
    

# 查并计算
@router.post("/member/{id}/caijin")
@require_token('getListMember,GET')
async def get_member(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=Member, id=id)
    try:
        new_caijin = 0
        for q in query.caijins:
            new_caijin = new_caijin + decimal.Decimal(q.money)
        
        query.total_caijin_money = new_caijin


        db.commit()
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='计算错误')
    return Success()



# 增
@router.post("/member")
@require_token('createMember,POST')
async def create_member(request: Request, item: CreateMemberSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    '''------------------------------------------------'''
    # # 如果不是超级用户
    # if not current_user.is_super:
    #     # 获取当前用户所属组
    #     userGroups = [ g.id for g in current_user.groups]
        
    #     # 判断如果数据不是用户所属组，不允许修改
    #     if item.owner_id not in userGroups:
    #         raise HTTPException(status_code=403, detail='不允许创建其他部门数据')
    '''------------------------------------------------'''
    
    username = str(item.username.replace(" ",""))
    is_exits,_ = await Crud.get_items(db=db, model=Member,other_filter=[and_(Member.username==username, Member.owner_id==item.owner_id)])

    if is_exits:
        raise HTTPException(status_code=403, detail=f'此部门已存在: {item.username}')

    query = await Crud.create_item(
            db=db, 
            model=Member, 
            channel_code=item.channel_code,
            username=username, 
            description=item.description,
            first_name=current_user.username,
            tags = db.query(Tag).filter(Tag.id.in_(item.tag_id)).all() if item.tag_id else [],
            owner_id=item.owner_id,
            total_in_money=item.total_in_money,
            total_out_money=item.total_out_money,
            total_before_two_in_money=item.total_before_two_in_money,
            total_before_two_throw_money=item.total_before_two_throw_money,
            total_before_two_out_money=item.total_before_two_out_money,
            total_before_two_wax_money=item.total_before_two_in_money - item.total_before_two_out_money,
            total_wax_money=item.total_in_money - item.total_out_money,
            register_at=item.register_at,
            last_login_at=item.last_login_at,
            register_ip=item.register_ip,
            last_login_ip=item.last_login_ip,
    )
    return Success(data=jsonable_encoder(query))


# 删
@router.delete("/member/{id}")
@require_token('deleteMember,DELETE')
async def del_member(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    # # 如果不是超级用户
    # if not current_user.is_super:
    #     # 获取当前用户所属组
    #     userGroups = [ g.id for g in current_user.groups]
        
    #     # 获取需要修改数据的归属部门
    #     obj = await Crud.show_item(db, Member, id)
        
    #     # 判断如果数据不是用户所属组，不允许修改
    #     if obj.owner_id not in userGroups:
    #         raise HTTPException(status_code=403, detail='不允许删除其他部门数据')
    '''------------------------------------------------'''

    await Crud.delele_item(db=db, model=Member, id=id, recover=True, last_name=current_user.username)
    return Success()



# 改
@router.put("/member/{id}")
@require_token('modifyMember,PUT')
async def update_member(request: Request, item: CreateMemberSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):


    username = str(item.username.replace(" ",""))

    _exists,_total = await Crud.get_items(db=db,model=Member, other_filter=[and_(Member.username==username, Member.owner_id==item.owner_id)])
    if _total > 1:
       raise HTTPException(status_code=400, detail=f'{item.username} 存在多个相同的数据') 
    elif _total == 1 and _exists[0].id != id:
        raise HTTPException(status_code=400, detail=f'{item.username} 已存在') 
        

    # 北京时间
    '''------------------------------------------------'''
    # # 如果不是超级用户
    # if not current_user.is_super:
    #     # 获取当前用户所属组
    #     userGroups = [ g.id for g in current_user.groups]
        
    #     # 获取需要修改数据的归属部门
    #     obj = await Crud.show_item(db, Member, id)
        
    #     # 判断如果数据不是用户所属组，不允许修改
    #     if obj.owner_id not in userGroups:
    #         raise HTTPException(status_code=403, detail='不允许修改其他部门数据')
    '''------------------------------------------------'''


    query = await Crud.update_item(
                db=db, 
                id=id,
                model=Member,
                username=username, 
                channel_code=item.channel_code,
                description=item.description,
                last_name=current_user.username,
                updated_at=get_today(hms=True),
                tags = db.query(Tag).filter(Tag.id.in_(item.tag_id)).all() if item.tag_id else [],
                owner_id=item.owner_id,
                total_in_money=item.total_in_money,
                total_out_money=item.total_out_money,
                total_before_two_in_money=item.total_before_two_in_money,
                total_before_two_throw_money=item.total_before_two_throw_money,
                total_before_two_out_money=item.total_before_two_out_money,
                total_before_two_wax_money=item.total_before_two_in_money - item.total_before_two_out_money,
                total_wax_money=item.total_in_money - item.total_out_money,
                register_at=item.register_at,
                last_login_at=item.last_login_at,
                register_ip=item.register_ip,
                last_login_ip=item.last_login_ip,
            )
    return Success(data=jsonable_encoder(query))




# 添加测试数据
# @router.post("/member/test/member")
# async def test_member(db: Session = Depends(get_db)):
#     _testList = []

#     import time

#     start_time = time.time()
#     sum = 0

#     for i in range(1,200000):
#         _testList.append({
#             'username': f'd{i}',
#             "channel_code": f'code{i}',
#             "owner_id": 2,
#             "total_in_money": f"{i}",
#             "total_out_money": f"{i}",
#             "total_before_two_in_money": f"{i}",
#             "total_before_two_throw_money": f"{i}",
#             "total_before_two_out_money": f"{i}",
#             "total_before_two_wax_money": f"{i}",
#             "total_wax_money": f"{i}",
#             "register_at": get_today(hms=True),
#             "last_login_at": get_today(hms=True),
#             "register_ip": "8.8.8.8",
#             "last_login_ip": "8.8.8.8",
#         })
#         sum += i

#     db.execute(
#             Member.__table__.insert(),
#             _testList
#         )

#     db.commit()
#     end_time = time.time()
#     return Success(msg=end_time-start_time)