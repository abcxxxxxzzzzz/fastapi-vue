from fastapi import APIRouter,Depends,Request,HTTPException,UploadFile,File,Form,Query
from fastapi.encoders import jsonable_encoder
from api.models import Group, RecordOutMoney,ReceState
from api.schemas import CreateRecordOutMoneySchema, UpdateRecordOutMoneyStatusSchema, ChangeDescriptionRecordOutMoneySchema, DoneRecordOutMoneySchema,batchDeleteRecordOutMoneySchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud
from sqlalchemy.orm import Session 
from api.utils import Success, get_today
from api.services import LoginCrud
from sqlalchemy.sql import and_,or_
from api.utils.logs import logger
import uuid
import pathlib
from api.configs.config import global_settings
from typing import Optional



router = APIRouter()



async def get_order_field(model, field, order_by):
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



# 列
@router.get("/recordoutmoney/list")
@require_token('getListRecordOutMoney,GET')
async def get_list_recordoutmoney(
    request: Request, 
    params: CommonQueryParams = Depends(),
    owner_id: Optional[int] = None,
    rece_id: Optional[int] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None, 
    start: Optional[str] = None, 
    end: Optional[str] = None, 
    field: Optional[str] = Query(None),
    order_by: Optional[str] = Query(None),
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db)
):
    # 获取用户归属组
    groups = current_user.groups
    groups_ids = list(map(lambda x:x.id, groups))
    
    
    # 关键词
    filters = []
    _k = getattr(params, 'keyword', None)
    if _k:
        filters.append(or_(
            RecordOutMoney.uid.like("%" + _k + "%"),
            RecordOutMoney.bank_name.like("%" + _k + "%"),
            RecordOutMoney.bank_card.like("%" + _k + "%"),
        ))

    # 提交人
    if first_name:
        filters.append(RecordOutMoney.first_name == first_name)
    
    # 操作人
    if last_name:
        filters.append(RecordOutMoney.last_name == last_name)

    # 搜索部门
    if owner_id:
        filters.append(RecordOutMoney.owner_id == owner_id)
    else:
        if not current_user.is_super:
            filters.append(RecordOutMoney.owner_id.in_(groups_ids))

    # 搜索接单状态
    if rece_id is not None:
        filters.append(RecordOutMoney.rece_state == rece_id)

    # 搜索申请日期
    if start:
        filters.append(RecordOutMoney.created_at.like(start + "%"))

    # 搜索操作日期
    if end:
        filters.append(RecordOutMoney.updated_at.like(end + "%"))

    # 排序
    if field and order_by:
        order_field = await get_order_field(RecordOutMoney, field, order_by)
    else:
        order_field = []


    if order_field:
        query, total = await Crud.get_items(db=db, model=RecordOutMoney, params=params, other_filter=filters, order_enable=True, order_field=order_field)
    else:
        query, total = await Crud.get_items(db=db, model=RecordOutMoney, params=params, other_filter=filters)


    # 获取用户
    f_query = await Crud.group_by(db=db, model=RecordOutMoney.first_name, _group_by=RecordOutMoney.first_name)
    l_query = await Crud.group_by(db=db, model=RecordOutMoney.last_name, _group_by=RecordOutMoney.last_name)



    

    searchReces = [
        {
            "id": ReceState.wait.value,
            "label": "未接单"
        },
        {
            "id": ReceState.rece.value,
            "label": "处理中"
        },
        {
            "id": ReceState.done.value,
            "label": "已支付"
        },
        {
            "id": ReceState.error.value,
            "label": "已作废"
        }
    ]


    reces = [
        {
            "id": ReceState.done.value,
            "label": "此单已支付"
        },
        {
            "id": ReceState.error.value,
            "label": "此单已作废"
        }
    ]


    data = {
        'list': jsonable_encoder(query),
        'totalCount': total,
        'groups': jsonable_encoder(groups, include=['id', 'name']),
        'f_users': jsonable_encoder(f_query),
        'l_users': jsonable_encoder(l_query),
        "reces": reces,
        "searchReces": searchReces,
    }
    return Success(data=data)



# 单
@router.get("/recordoutmoney/{id}/show")
@require_token('ShowRecordOutMoney,GET')
async def get_recordoutmoney(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=RecordOutMoney, id=id)
    return Success(data=jsonable_encoder(query))
    


# 增
@router.post("/recordoutmoney/create")
@require_token('CreateRecordOutMoney,POST')
async def create_recordoutmoney(request: Request, item: CreateRecordOutMoneySchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    # 获取用户归属组
    groups = current_user.groups
    groups_ids = list(map(lambda x:x.id, groups))
    
    if item.owner_id not in groups_ids:
        raise HTTPException(status_code=403, detail="不是所属部门，权限不足")
    
    query = await Crud.create_item(
            db=db, 
            model=RecordOutMoney, 
            owner_id=item.owner_id, 
            uid=item.uid, 
            bank_name=item.bank_name, 
            bank_owner=item.bank_owner, 
            bank_child=item.bank_child, 
            bank_card=item.bank_card, 
            out_money=item.out_money,
            first_name=current_user.username
    )
    return Success(data=jsonable_encoder(query))



# 删
@router.delete("/recordoutmoney/{id}/delete")
@require_token('DeleteRecordOutMoney,DELETE')
async def del_recordoutmoney(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # 获取用户归属组
    groups = current_user.groups
    groups_ids = list(map(lambda x:x.id, groups))
    
        
    before = await Crud.show_item(id=id, db=db, model=RecordOutMoney)
    if before.two_enter == 1:
        raise HTTPException(status_code=403, detail="信息已经确认,不允许删除,如需要删除，请联系管理员")

    if before.owner_id not in groups_ids:
        raise HTTPException(status_code=403, detail="不是所属部门，权限不足")

    if before.first_name != current_user.username:
        raise HTTPException(status_code=403, detail="不是你的订单，权限不足")

    await Crud.delele_item(db=db, model=RecordOutMoney, id=id)
    return Success()



# 改
@router.put("/recordoutmoney/{id}/update")
@require_token('UpdateRecordOutMoney,PUT')
async def update_recordoutmoney(request: Request, item: CreateRecordOutMoneySchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    # 获取用户归属组
    groups = current_user.groups
    groups_ids = list(map(lambda x:x.id, groups))

    before = await Crud.show_item(id=id,db=db, model=RecordOutMoney)
    if before.two_enter != 0:
        raise HTTPException(status_code=403, detail="信息已经确认,不允许再次修改")
    
    if before.owner_id not in groups_ids:
        raise HTTPException(status_code=403, detail="不是所属部门，权限不足")

    if before.first_name != current_user.username:
        raise HTTPException(status_code=403, detail="不是你的订单，权限不足")
    
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=RecordOutMoney, 
                owner_id=item.owner_id, 
                uid=item.uid, 
                bank_name=item.bank_name, 
                bank_owner=item.bank_owner, 
                bank_child=item.bank_child, 
                bank_card=item.bank_card, 
                out_money=item.out_money
            )
    return Success(data=jsonable_encoder(query))




# 二次确认
@router.post("/recordoutmoney/{id}/status")
@require_token('CreateRecordOutMoney,POST')
async def update_recordoutmoney_enter(request: Request, item: UpdateRecordOutMoneyStatusSchema, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    username = current_user.username
    groups = current_user.groups
    groups_ids = list(map(lambda x:x.id, groups))
    
    query,_ = await Crud.get_items(
            db=db, 
            model=RecordOutMoney,
            other_filter=[and_(RecordOutMoney.id==id, RecordOutMoney.first_name==username, RecordOutMoney.owner_id.in_(groups_ids))]
        )

    if query:
        if len(query) == 1 and query[0].two_enter == 0:
            if item.status != 1:
                raise HTTPException(status_code=400, detail='参数错误,只能 1 或者 0')
            query[0].two_enter = item.status
            query[0].rece_state = ReceState.wait.value
            try:
                db.commit()
                return Success(data=jsonable_encoder(query))
            except Exception as e:
                logger.error(str(e))
                db.rollback()
                raise HTTPException(status_code=500, detail="服务内部错误！")

        else:
            raise HTTPException(status_code=403, detail='权限不足，请刷新检查此订单是否已经确认过或者此订单不是自己的部门')
    else:
        raise HTTPException(status_code=404, detail='不是所属部门或权限不足')









# 确认接单
@router.post("/recordoutmoney/{id}/rece")
@require_token('ReceRecordOutMoney,POST')
async def update_recordoutmoney_rece(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    username = current_user.username
    groups = current_user.groups
    groups_ids = list(map(lambda x:x.id, groups))

    # 判断是否是指定部门的
    query,_ = await Crud.get_items(
            db=db, 
            model=RecordOutMoney,
            other_filter=[and_(RecordOutMoney.id==id, RecordOutMoney.owner_id.in_(groups_ids))]
        )

    if query:
        if len(query) == 1 and query[0].two_enter == 1 and query[0].rece_state == ReceState.wait.value:
            query[0].rece_state = ReceState.rece.value
            query[0].last_name = username
            try:
                db.commit()
                return Success(data=jsonable_encoder(query))
            except Exception as e:
                logger.error(str(e))
                db.rollback()
                raise HTTPException(status_code=500, detail="服务内部错误！")
        else:
            raise HTTPException(status_code=403, detail='权限不足，请刷新检查是否已经接单或者此订单不是自己的部门')

    else:
        raise HTTPException(status_code=404, detail='未找到需要更新的对象或权限不足')




# 回传图片
@router.post("/recordoutmoney/image/upload")
@require_token('uploadImgToRecordOutMoney,POST')
async def upload_recordoutmoney_img(request: Request, id: int = Form(...), img: UploadFile = File(...), current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    username = current_user.username
    groups = current_user.groups
    groups_ids = list(map(lambda x:x.id, groups))

    query,_ = await Crud.get_items(
            db=db, 
            model=RecordOutMoney,
            other_filter=[and_(RecordOutMoney.id==id,RecordOutMoney.owner_id.in_(groups_ids))]
        )

    if not query:
        raise HTTPException(status_code=404, detail='未找到此订单')

    if query[0].last_name != username:
        raise HTTPException(status_code=403, detail='此订单已被其他人接单')


    # 验证图片是否是规定后缀
    _suffix = ['jpg', 'png']
    imgbytes = await img.read()
    imgsuffix  = img.filename.split('.')[-1]
    if imgsuffix.lower() not in _suffix:
        raise HTTPException(status_code=400, detail='图片格式不正确, 请使用 jpg 或者 png 格式后缀')

    # 判断日期文件是否存在
    path = pathlib.Path(global_settings.upload_name + '/' + get_today())
    if not path.exists():
        path.mkdir()

    # 生成唯一 UUID 名字保存
    savefilename  = str(uuid.uuid1())
    savepath = open(path.joinpath(savefilename + '.' + imgsuffix.lower()), 'wb')
    savepath.write(imgbytes)
    savepath.close()

    return Success(data={"path": savepath.name})

    # query.img_path = savepath.name
    # query.rece_state = ReceState.done.value
    # try:
    #     db.commit()
    #     return {'filename': img.filename}
    # except Exception as e:
    #     db.rollback()
    #     from api.utils import logger
    #     logger.error(str(e))
    #     raise HTTPException(status_code=500, detail="保存图片路径失败")
    


# 确认订单
@router.post("/recordoutmoney/{id}/done")
@require_token('uploadImgToRecordOutMoney,POST')
async def upload_recordoutmoney_img(request: Request, id: int, item: DoneRecordOutMoneySchema,  current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    username = current_user.username
    groups = current_user.groups
    groups_ids = list(map(lambda x:x.id, groups))

    query,_ = await Crud.get_items(
            db=db, 
            model=RecordOutMoney,
            other_filter=[and_(RecordOutMoney.id==id, RecordOutMoney.last_name==username, RecordOutMoney.owner_id.in_(groups_ids))]
        )
        

    if not query:
        raise HTTPException(status_code=404, detail='未找到此订单或权限不足')


    query = query[0]    
    # query = await Crud.show_item(db=db, model=RecordOutMoney, id=id)


    if not query:
        raise HTTPException(status_code=404, detail='此订单不存在')

    if query.rece_state == ReceState.done.value or query.rece_state == ReceState.error.value:
        raise HTTPException(status_code=400, detail='已结单')

    if query.two_enter != 1:
        raise HTTPException(status_code=400, detail='此订单未二次确认')

    if query.rece_state != ReceState.rece.value:
        raise HTTPException(status_code=400, detail='此订单未知')

    if item.rece == ReceState.done.value and  item.img_path == '': 
        raise HTTPException(status_code=400, detail='如果已支付,请上传支付截图')

    if item.rece < 0 or item.rece > 4:
        raise HTTPException(status_code=400, detail='数据不合法')


    query.img_path    = item.img_path
    query.rece_state  = item.rece
    query.description = item.description
    query.updated_at  = get_today(hms=True)
    try:
        db.commit()
        return Success()
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="服务内部错误,请联系管理员")


    

# 修改备注
@router.put("/recordoutmoney/{id}/desc")
@require_token('uploadImgToRecordOutMoney,POST')
async def upload_recordoutmoney_img(request: Request, id: int, item: ChangeDescriptionRecordOutMoneySchema,  current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    username = current_user.username
    groups = current_user.groups
    groups_ids = list(map(lambda x:x.id, groups))

    query,_ = await Crud.get_items(
            db=db, 
            model=RecordOutMoney,
            other_filter=[and_(RecordOutMoney.id==id,RecordOutMoney.last_name==username,RecordOutMoney.owner_id.in_(groups_ids))]
        )

    # query = await Crud.show_item(db=db, model=RecordOutMoney, id=id)

    if not query:
        raise HTTPException(status_code=404, detail='此订单不存在')

    query[0].description = item.description
    try:
        db.commit()
        return Success()
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="服务内部错误,请联系管理员")




# 批量删除
@router.post("/recordoutmoney/batch/delete")
@require_token('DeleteBatchRecordOutMoney,POST')
async def batch_delete_caijin(request: Request, item: batchDeleteRecordOutMoneySchema,current_user: LoginCrud.verify_token = Depends(),  db: Session = Depends(get_db)):
    await Crud.multi_delete(db=db, model=RecordOutMoney, ids=item.ids, multi_delete=True)
    return Success()
