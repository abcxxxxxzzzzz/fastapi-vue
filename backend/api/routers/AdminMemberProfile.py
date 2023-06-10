from fastapi import APIRouter,Depends,Request,Query,HTTPException
from fastapi.encoders import jsonable_encoder
from api.models import MemberProfile,Tag,Group,taskRecord
from api.schemas import CreateMemberProfileSchema,batchImportMemberProfileSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud,MemberProfileServices
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from api.utils import Success,get_today
from api.services import LoginCrud
from typing import Optional
from datetime import datetime, timedelta
import uuid
from api.dependen.lockRedis import lock
from api.exts import Schedule
from api.tasks.ExcelImportMemberProfileTask import import_excel


router = APIRouter()


# 导入者，更新者
@router.get("/member/profile/people")
@require_token('getListMemberProfile,GET')
async def get_member_profile_people(request: Request, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    # 部门
    tags,_ = await Crud.get_items(db=db, paging=False, model=Tag)
    tags = jsonable_encoder(tags, include=['id', 'name', 'color'])
    return Success(data={ 'tags' : tags})




# 标签
@router.get("/member/profile/tags")
@require_token('getListMemberProfile,GET')
async def get_member_profile_tag(request: Request, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    # 部门
    tags,_ = await Crud.get_items(db=db, paging=False, model=Tag)
    tags = jsonable_encoder(tags, include=['id', 'name', 'color'])
    return Success(data={ 'tags' : tags})




# 部门
@router.get("/member/profile/groups")
@require_token('getListMemberProfile,GET')
async def get_member_profile_group(request: Request, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    # 部门
    groups,_ = await Crud.get_items(db=db, paging=False, model=Group)
    groups = jsonable_encoder(groups, include=['id', 'name'])
    return Success(data={ 'groups' : groups})


# 列
@router.get("/member/profile/list/")
@require_token('getListMemberProfile,GET')
async def get_member_profile_list(request: Request, 
    first_name: Optional[str] = Query(None), 
    last_name: Optional[str] = Query(None), 
    owner_id: Optional[int] = Query(None),
    owner_tag_id: Optional[str] = Query(None), 
    field: Optional[str] = Query(None),
    order_by: Optional[str] = Query(None),
    params: CommonQueryParams = Depends(),
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db)
):
    # query, total = await Crud.get_items(db=db,model=MemberProfile, params=params)


    # print(first_name, last_name, owner_id,owner_tag_id, field, order_by)
    # 设置搜索部门
    if owner_id is not None:
        setattr(params, 'owner_id', owner_id) 

    # 标签搜索转换
    if bool(owner_tag_id):
        _tags = list(map(int, owner_tag_id.split(','))) or list[int(owner_tag_id)]
        setattr(params, '_tags', _tags) 

    # 设置搜索创建者
    if first_name is not None:
        setattr(params, '_first_name', first_name) 

    # 设置搜索更新者
    if last_name is not None:
        setattr(params, '_last_name', last_name) 

    # 设置排序方式
    # if field and order_by:
    #     await MemberProfileServices.get_order_field(
    #         model=MemberProfile,
    #         field=field,
    #         order_by=order_by,
    #     )


    # 返回总数据
    data = await MemberProfileServices.get_list(
            db=db, 
            model=MemberProfile,
            params=params, 
            field=field,
            order_by=order_by,
    )
    return Success(data=data)



    # _list = jsonable_encoder(query)
    # _total = total
    # data = {
    #     'list': _list,
    #     'totalCount': _total,
    # }
    # return Success(data=data)

# 查单
@router.get("/member/profile/{id}/show")
@require_token('getMemberProfile,GET')
async def get_member_profile(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=MemberProfile, id=id)
    return Success(data=jsonable_encoder(query))
    
# 增单
@router.post("/member/profile/create")
@require_token('createMemberProfile,POST')
async def create_member_profile(request: Request, item: CreateMemberProfileSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    
    is_exits,_ = await Crud.get_items(db=db, model=MemberProfile,other_filter=[and_(MemberProfile.account==item.account, MemberProfile.owner_id==item.owner_id)])

    if is_exits:
        raise HTTPException(status_code=400, detail=f'此部门已存在: {item.account}')
    
    
    query = await Crud.create_item(
            db=db, 
            model=MemberProfile, 
            code=item.code, 
            account=item.account,
            account_id=item.account_id,
            realname=item.realname,
            iphone_num=item.iphone_num,
            contact=item.contact,
            bank_number=item.bank_number,
            description=item.description,
            first_name=current_user.username,
            owner_id=item.owner_id,
            tags=db.query(Tag).filter(Tag.id.in_(item.tag_id)).all() if item.tag_id else [],
    )
    return Success(data=jsonable_encoder(query))


# 删单
@router.delete("/member/profile/{id}/delete")
@require_token('deleteMemberProfile,DELETE')
async def del_member_profile(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    
    query = await Crud.show_item(db=db, model=MemberProfile, id=id)
    # 删除标签关联
    query.members = []


    await Crud.delele_item(db=db, model=MemberProfile, id=id)
    return Success()



# 改单
@router.put("/member/profile/{id}/update")
@require_token('updateMemberProfile,PUT')
async def update_member_profile(request: Request, item: CreateMemberProfileSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    
    _exists,_total = await Crud.get_items(db=db,model=MemberProfile, other_filter=[and_(MemberProfile.account==item.account, MemberProfile.owner_id==item.owner_id)])
    if _total > 1:
       raise HTTPException(status_code=400, detail=f'{item.account} 存在多个相同的数据') 
    elif _total == 1 and _exists[0].id != id:
        raise HTTPException(status_code=400, detail=f'{item.account} 已存在') 
        

    
    
    query = await Crud.update_item(
                db=db, 
                model=MemberProfile,
                id=id,
                code=item.code, 
                account=item.account,
                account_id=item.account_id,
                realname=item.realname,
                iphone_num=item.iphone_num,
                contact=item.contact,
                bank_number=item.bank_number,
                description=item.description,
                last_name=current_user.username,
                owner_id=item.owner_id,
                tags=db.query(Tag).filter(Tag.id.in_(item.tag_id)).all() if item.tag_id else [],
                updated_at=get_today(hms=True)

            )
    return Success(data=jsonable_encoder(query))



# 批量导入
@router.post("/member/profile/batch/import")
@require_token('importExcelMemberProfile,POST')
@lock('excel_import_member_profile')
async def batch_import_profile(request: Request, item: batchImportMemberProfileSchema,  current_user: LoginCrud.verify_token = Depends(),  db: Session = Depends(get_db)):

    before_30_min = next_cmd = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    _path = request.scope['path']
    _uuid = uuid.uuid1().hex
    path = f'{_path}_{_uuid}'

    # 批量导入前 30 分钟查询是否存在有人提交了任务
    is_exist_task,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path.like(_path + "%"), taskRecord.progress != 100, taskRecord.created_at > before_30_min)])
    if is_exist_task:
        raise HTTPException(status_code=400, detail=f"{is_exist_task[0].created_at} {is_exist_task[0].first_name} 任务进度 {int(is_exist_task[0].progress)}% 正在运行中 , 请等任务完成后或者5分钟后再次提交")


    # 查询是否有只有一个部门
    upload_group = list(set(map(lambda x:str(x.get('owner','')).replace(" ",""), item.importData)))
    if len(upload_group) > 1:
        raise HTTPException(status_code=400, detail='每次上传只允许上传一个部门数据')


    # 查询部门是否存在
    is_group,_ = await Crud.get_items(db=db, model=Group, other_filter=[Group.name==upload_group[0]])
    if not is_group:
        raise  HTTPException(status_code=400, detail='部门不存在')


    # 当前时间的后 10 秒执行导入
    next_cmd = (datetime.now() + timedelta(seconds=5)).strftime("%Y-%m-%d %H:%M:%S")
    Schedule.add_job(import_excel, 'date',  run_date=next_cmd,  misfire_grace_time=3600, args=[is_group[0].id, path, current_user.username, item.importData])

    return Success(data={'task_id': path })





# 获取计划任务
@router.get("/member/profile/batch/import")
@require_token('importExcelMemberProfile,POST')
async def batch_import_profile(request: Request, task_id: str = Query(...),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # _path = request.scope['path']

    _rdata,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path==task_id, taskRecord.first_name==current_user.username)])
    if _rdata:
        return Success(data={ "task": jsonable_encoder(_rdata[0])})
    else:
        return Success(data={ "task": {'progress': 0}})



    # insert_total, update_total, error_data = await MemberProfileServices.import_excel(db=db, data=item.importData, current_user=current_user)


    # data = {
    #     "insert_total": insert_total,
    #     "update_total": update_total,
    #     "error_data": error_data,
    # }

    # return Success(data=data)

