import decimal
from fastapi import APIRouter,Depends,Request,Query,BackgroundTasks,HTTPException,WebSocket,WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from api.models import MemberCaiJin,Member,Group,User,taskRecord
from api.schemas import CreateMemberCaiJinSchema,batchDeleteMemberCaiJinSchema,batchImportMemberCaiJinSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud,LoginCrud,MemberCaiJinServices
from sqlalchemy.orm import Session 
from api.utils import Success,get_today, WebSocketManager
from typing import Optional
from sqlalchemy.sql import and_
from api.exts import Schedule
from api.tasks import excel_import_caijin
from datetime import datetime, timedelta
import uuid
from api.dependen.lockRedis import lock


router = APIRouter()



# 只限关键词搜索
@router.get("/member/caijin/search/")
@require_token('getMemberCaiJinList,GET')
async def get_search_keyword(request: Request, 
    q: Optional[str] = Query(None), 
    s: Optional[int] = Query(None),
    params: CommonQueryParams = Depends(),
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db)
):
    



    if s is None:
        result, _ = await Crud.get_items(db=db, model=Member,  params=params,other_filter=[Member.username.like("%" + q +"%")]) 
    else:
        result, _ = await Crud.get_items(db=db, model=Member,  params=params,other_filter=[and_(Member.username.like("%" + q +"%"), Member.owner_id==s)]) 

    data = jsonable_encoder(result, include=['id', 'username'])
    return Success(data=data)




# 列
@router.get("/member/caijin/list")
@require_token('getMemberCaiJinList,GET')
async def get_caijin_list(request: Request, 
    asynckeyword: Optional[str] = Query(None), 
    params: CommonQueryParams = Depends(),
    member_id: Optional[int] = Query(None),
    owner_id: Optional[int] = Query(None),
    owner_tag_id: Optional[str] = Query(None), 
    field: Optional[str] = Query(None),
    order_by: Optional[str] = Query(None),
    first_name: Optional[str] = Query(None), 
    last_name: Optional[str] = Query(None), 
    start_end: Optional[str] = Query(None), 
    update_start_end: Optional[str] = Query(None), 
    current_user: LoginCrud.verify_token = Depends(),
    db: Session = Depends(get_db)
):
    

    filters = []
    # 是否搜索查询数据
    if asynckeyword:
        _asynck = asynckeyword.split(',') or list[asynckeyword]
        filters.append(MemberCaiJin.member_id.in_(_asynck))


    # 如果搜索会员,
    if member_id:
        setattr(params, 'member_id', member_id) 

    # 设置搜索部门
    if owner_id is not None:
        setattr(params, 'owner_id', owner_id) 

    # 标签搜索
    if bool(owner_tag_id):
        _tags = list(map(int, owner_tag_id.split(','))) or list[int(owner_tag_id)]
        setattr(params, '_tags', _tags) 

    # 设置搜索创建时间
    if start_end:
        setattr(params, '_start_end', start_end) 

    # 设置搜索更新时间
    if update_start_end:
        setattr(params, '_update_start_end', update_start_end) 

    # 设置搜索导入人
    if first_name:
        setattr(params, '_first_name', first_name) 


    # 设置搜索更新人
    if last_name:
        setattr(params, '_last_name', last_name) 

    # print(field, order_by)
    # 如果点击排序获取排序
    # if field and order_by:
    #     await MemberCaiJinServices.get_order_field(
    #         model=MemberCaiJin,
    #         field=field,
    #         order_by=order_by,
    #     )
    
    
    
    # query, total = await Crud.get_items(db=db,model=MemberCaiJin, params=params)
    # _list = jsonable_encoder(query)
    # _total = total
    query, total =  await MemberCaiJinServices.get_list(db=db,model=MemberCaiJin, params=params, filters=filters,field=field,order_by=order_by,) 

    # 获取群组
    # g_query, _ = await Crud.get_items(db=db,model=Group, paging=False)
    # print(jsonable_encoder(current_user.groups)) 


    # 获取用户
    f_query = await Crud.group_by(db=db, model=MemberCaiJin.first_name, _group_by=MemberCaiJin.first_name)
    l_query = await Crud.group_by(db=db, model=MemberCaiJin.last_name, _group_by=MemberCaiJin.last_name)


    data = {
        'list': query,
        'totalCount': total,
        'groups': jsonable_encoder(current_user.groups, include=['id', 'name']),
        'f_users': jsonable_encoder(f_query),
        'l_users': jsonable_encoder(l_query),
    }
    return Success(data=data)



# 查
@router.get("/member/caijin/{id}/show")
@require_token('getMemberCaiJinShow,GET')
async def get_member(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=MemberCaiJin, id=id)
    return Success(data=jsonable_encoder(query))


# 添
@router.post("/member/caijin/create")
@require_token('getMemberCaiJinCreate,POST')
async def create_member_caijin(request: Request, item: CreateMemberCaiJinSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    _member_g,_c = await Crud.get_items(db=db, model=Member, other_filter=[Member.id==item.member_id])
    if not _c:
        raise HTTPException(status_code=400, detail='ID不存在')
    
    _groups = list(map(lambda x:x.id, current_user.groups))

    if _member_g[0].owner.id not in _groups:
        raise HTTPException(status_code=400, detail='权限不足，不允许添加到其他部门')
    

    # 先获取会员是否存在，如果存在则计算金额，随创建一起提交
    _mq = await Crud.show_item(db=db, model=Member, id=item.member_id)
    _mq.total_caijin_money = _mq.total_caijin_money + decimal.Decimal(item.money)
    _mq.updated_at= get_today(hms=True)


    query = await Crud.create_item(
            db=db, 
            model=MemberCaiJin, 
            member_id=item.member_id, 
            source_id=item.source_id,
            money=item.money,
            description=item.description,
            first_name=current_user.username,
    )


    
    # _mq.total_caijin_money = _mq.total_caijin_money + item.money
    # db.commit(_mq)
    return Success(data=jsonable_encoder(query))


# 更
@router.put("/member/caijin/{id}/update")
@require_token('getMemberCaiJinUpdate,PUT')
async def update_member_caijin(request: Request, item: CreateMemberCaiJinSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):



    _member_g,_c = await Crud.get_items(db=db, model=Member, other_filter=[Member.id==item.member_id])
    if not _c:
        raise HTTPException(status_code=400, detail='ID不存在')
    
    _groups = list(map(lambda x:x.id, current_user.groups))

    if _member_g[0].owner.id not in _groups:
        raise HTTPException(status_code=400, detail='权限不足，不允许添加到其他部门')
    

    # 先获取彩金的原始金额
    _old_q = await Crud.show_item(db=db, model=MemberCaiJin, id=id)

    # 先获取会员是否存在，如果存在则计算金额，减去旧金额，加上新金额，一起提交
    _mq = await Crud.show_item(db=db, model=Member, id=item.member_id)
    _mq.total_caijin_money = _mq.total_caijin_money - _old_q.money + decimal.Decimal(item.money)
    _mq.updated_at= get_today(hms=True)

    query = await Crud.update_item(
                db=db, 
                id=id,
                model=MemberCaiJin,
                member_id=item.member_id, 
                source_id=item.source_id,
                money=decimal.Decimal(item.money),
                description=item.description,
                last_name=current_user.username,
                updated_at= get_today(hms=True)
            )
    return Success(data=jsonable_encoder(query))
 

# 删 
@router.delete("/member/caijin/{id}/delete")
@require_token('getMemberCaiJinDelete,DELETE')
async def del_member_caijin(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    _groups = list(map(lambda x:x.id, current_user.groups))
    
    is_exists = await Crud.show_item(db=db, model=MemberCaiJin, id=id)
    _g_id = is_exists.members.owner.id

    if _g_id not in _groups:
        raise HTTPException(status_code=403, detail='权限不足，不允许修改到其他部门')


    await Crud.delele_item(db=db, model=MemberCaiJin, id=id)
    return Success()

 

# 批量删除
@router.post("/member/caijie/batch/delete")
@require_token('getMemberCaiJinBatchDelete,POST')
async def batch_delete_caijin(request: Request, item: batchDeleteMemberCaiJinSchema,current_user: LoginCrud.verify_token = Depends(),  db: Session = Depends(get_db)):
    await Crud.multi_delete(db=db, model=MemberCaiJin, ids=item.ids, multi_delete=True)
    return Success()



# 批量导入
@router.post("/member/caijie/batch/import")
@require_token('getMemberCaiJinBatchImport,POST')
@lock('excel_import_caijin')
async def batch_import_caijin(request: Request, item: batchImportMemberCaiJinSchema, background_task:BackgroundTasks, current_user: LoginCrud.verify_token = Depends(),  db: Session = Depends(get_db)):

    before_30_min = next_cmd = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    _path = request.scope['path']
    _uuid = uuid.uuid1().hex
    path = f'{_path}_{_uuid}'

    # 批量导入前查询是否存在有人提交了任务
    is_exist_task,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path.like(_path + "%"), taskRecord.progress != 100,taskRecord.created_at > before_30_min)])
    if is_exist_task:
        raise HTTPException(status_code=400, detail=f"{is_exist_task[0].created_at} {is_exist_task[0].first_name} 任务进度 {int(is_exist_task[0].progress)}% 正在运行中 , 请等任务完成后或者5分钟后再次提交")


    # 查询组是否存在
    upload_group = list(set(map(lambda x:str(x.get('owner','')).replace(" ",""), item.importData)))
    if len(upload_group) > 1:
        raise HTTPException(status_code=400, detail='每次上传只允许上传一个部门数据')


    # 查询部门是否存在
    is_group,_ = await Crud.get_items(db=db, model=Group, other_filter=[Group.name==upload_group[0]])
    if not is_group:
        raise  HTTPException(status_code=400, detail='部门不存在')


    

    # 根据实际时间生成唯一的UUID，保存任务详情到数据库
    # _before =  taskRecord(path=f'{path}_{uuid}', task_name='彩金批量导入', progress=0, first_name=current_user)

    
    # await Crud.create_item(db=db, model=taskRecord, path=path,  task_name='彩金批量导入', progress=0, first_name=current_user.username)

    
    # 当前时间的后 10 秒执行导入
    next_cmd = (datetime.now() + timedelta(seconds=5)).strftime("%Y-%m-%d %H:%M:%S")
    # next_cmd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Schedule.add_job(excel_import_caijin, 'date',  run_date=next_cmd, misfire_grace_time=3600, args=[is_group[0].id, path, current_user.username, item.importData])
    return Success(data={'task_id': path })



# # 获取计划任务
@router.get("/member/caijie/batch/import")
@require_token('getMemberCaiJinBatchImport,POST')
async def batch_import_caijin(request: Request, task_id: str = Query(...),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):


    _rdata,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path==task_id, taskRecord.first_name==current_user.username)])
    if _rdata:
        return Success(data={ "task": jsonable_encoder(_rdata[0])})
    else:
        return Success(data={ "task": {'progress': 0}})





# # 获取计划任务
# @router.websocket("/member/caijie/batch/import/ws")
# async def batch_import_caijin(websocket: WebSocket, token: str = Query(...), task_id: str = Query(), db: Session = Depends(get_db)):


#     username = 'admin'
#     task_id = task_id
#     print(username, task_id)

#     await WebSocketManager.connect(websocket)
#     try:
#         while True:
#             if username  and task_id:
#                 _rdata,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path==task_id, taskRecord.first_name==username)])
#                 print(_rdata)
#                 import time
#                 time.sleep(1)
#                 if _rdata:
#                     progress = _rdata[0].progress
#                 else:
#                     progress = '0'
#                 await WebSocketManager.send_message(progress,websocket)
#                 if int(progress) == 100:
#                     WebSocketManager.disconnect(websocket)
#                     break
#             else:
#                 await WebSocketManager.send_message('false')
#     except WebSocketDisconnect:
#         WebSocketManager.disconnect(websocket)
#         await WebSocketManager.broadcast(f"Client #'task_id' left the chat")





