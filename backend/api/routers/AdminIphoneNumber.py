from fastapi import APIRouter,Depends,Request,Query,HTTPException,BackgroundTasks
from fastapi.encoders import jsonable_encoder
from api.models import IphoneNumber, taskRecord
from api.schemas import CreateIphoneNumberSchema,batchIphoneNumberSchema,batchImportIphoneNumberSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud,IphoneNumberServices
from sqlalchemy.orm import Session 
from api.utils import Success, get_today,is_valid_phone_number,get_progress,setToRedis,getFromRedis
from api.services import LoginCrud
from typing import Optional
from sqlalchemy.sql import and_

router = APIRouter()



@router.get("/iphone/number/list")
@require_token('getListIphoneNumber,GET')
async def get_iphone_number_list(
    request: Request, 
    field: Optional[str] = Query(None),
    order_by: Optional[str] = Query(None),
    first_name: Optional[str] = Query(None), 
    last_name: Optional[str] = Query(None), 
    start_end: Optional[str] = Query(None), 
    update_start_end: Optional[str] = Query(None), 
    params: CommonQueryParams = Depends(),
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db)
):


    

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
    if field and order_by:
        await IphoneNumberServices.get_order_field(
            model=IphoneNumber,
            field=field,
            order_by=order_by,
        )
    
    
    
    # query, total = await Crud.get_items(db=db,model=MemberCaiJin, params=params)
    # _list = jsonable_encoder(query)
    # _total = total
    query, total =  await IphoneNumberServices.get_list(db=db,model=IphoneNumber, params=params) 



    # 获取用户
    f_query = await Crud.group_by(db=db, model=IphoneNumber.first_name, _group_by=IphoneNumber.first_name)
    l_query = await Crud.group_by(db=db, model=IphoneNumber.last_name, _group_by=IphoneNumber.last_name)


    data = {
        'list': query,
        'totalCount': total,
        'f_users': jsonable_encoder(f_query),
        'l_users': jsonable_encoder(l_query),
    }
    return Success(data=data)


    # query, total = await Crud.get_items(db=db,model=IphoneNumber, params=params)
    # _list = jsonable_encoder(query)
    # _total = total
    # data = {
    #     'list': _list,
    #     'totalCount': _total
    # }


    # return Success(data=data)


@router.get("/iphone/number/{id}/show")
@require_token('getIhoneNumber,GET')
async def get_iphone_number(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=IphoneNumber, id=id)
    return Success(data=jsonable_encoder(query))
    

@router.post("/iphone/number/create")
@require_token('createIphoneNumber,POST')
async def create_iphone_number(request: Request, item: CreateIphoneNumberSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    query = await Crud.create_item(
            db=db, 
            model=IphoneNumber, 
            number=item.number, 
            first_name=current_user.username,
    )
    return Success(data=jsonable_encoder(query))



@router.delete("/iphone/number/{id}/delete")
@require_token('deleteIphoneNumber,DELETE')
async def del_iphone_number(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    await Crud.delele_item(db=db, model=IphoneNumber, id=id)
    return Success()




@router.put("/iphone/number/{id}/update")
@require_token('updateIphoneNumber,PUT')
async def update_iphone_number(request: Request, item: CreateIphoneNumberSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):    
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=IphoneNumber,
                number=item.number, 
                last_name=current_user.username,
                updated_at=get_today(hms=True)
            )
    return Success(data=jsonable_encoder(query))

@router.post("/iphone/number/batch/delete")
@require_token('batchDeleteIphoneNumber,POST')
async def batch_del_iphone_number(request: Request, item: batchIphoneNumberSchema , current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    await Crud.multi_delete(db=db, model=IphoneNumber, ids=item.ids, multi_delete=True)
    return Success()


# 文件上传批量导入
@router.post("/iphone/number/batch/import")
@require_token('batchImportIphoneNumber,POST')
async def batch_import_iphone_number(request: Request, item: batchImportIphoneNumberSchema, background_task:BackgroundTasks,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    _path = request.scope['path']
    # IphoneNumberServices.get_date(_path, db, current_user, item)
    
    background_task.add_task(IphoneNumberServices.get_date, _path, db, current_user, item)

    return Success(msg='已添加到后台任务')







# # 获取计划任务
@router.get("/iphone/number/batch/import")
@require_token('getListIphoneNumber,GET')
async def iphone_number_task(request: Request, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    _path = request.scope['path']

    _rdata,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path==_path, taskRecord.first_name==current_user.username)])

    # print(_rdata[0].progress)
    if _rdata:
        progress = _rdata[0].progress
        return Success(data={'progress': progress})
    else:
        return Success(data={'progress': 100})