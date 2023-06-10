from fastapi import APIRouter,Depends,Request,Query,HTTPException,BackgroundTasks
from fastapi.encoders import jsonable_encoder
from api.models import keyWord,searchKeyWord,taskRecord
from api.schemas import CreateKeyWordSchema,batchCreateKeyWordSchema,batchDeleteKeyWordSchema,batchUpdataKeyWordSchema,batchConditionUpdataKeyWordSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud
from sqlalchemy.orm import Session 
from api.utils import Success,get_today
from api.services import LoginCrud
from typing import Optional,Union
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from api.utils.logs import logger
import random
from sqlalchemy import and_
import uuid
from api.tasks import get_pro

router = APIRouter()



# @router.get("/keyword/test/test")
# async def get_kewword(request: Request,  db: Session = Depends(get_db)):

#     # 所有数据
#     _all = db.query(keyWord.name).filter(keyWord.status==1).all()


#     # 去重后数据
#     qs = db.query(keyWord.name).filter(keyWord.status==1).distinct().all()


#     # 需要删除的数据
#     _del_name = list(set(_all).difference(set(qs)))

    
#     _del_ids = []
#     for q in _del_name:
#         # 先获取所有数据,让数据库只暴露一条数据
#         _s = db.query(keyWord).filter(and_(keyWord.name.ilike(q.name), keyWord.status==1)).all()[1:]

#         # 判断数量是否大于 1
#         if _s:
#             print(jsonable_encoder(_s))
#             _del_ids = _del_ids + list(map(lambda x:x.id, _s))

#         # break


#     # 开始删除

#     _start_del = db.query(keyWord).filter(and_(keyWord.status==1, keyWord.id.in_(_del_ids))).all()
#     for i in _start_del:
#         db.delete(i)
#     db.commit()
    
    
#     return Success(data=jsonable_encoder(_del_name))
    
def excelField():
    _field = {
            'name': "关键词名称", "type": "库存类型", 
            "created_at": "导入时间", "updated_at": "更新时间", 
            "first_name":"导入人", "status": "关键词状态", 
            "search_user":"搜索人", "last_name":"更新人",
            "searchkeywords": "关键词分类"
        }
    _update = {
            'status': {"-2": "未查询", "-1": "正在查询", "1": "已查询"}, 
            'searchkeywords': ['en'], # 获取关联表中其中一个值，必须序列化数据也是列表
        }
    return _field, _update



# 获取所有关键词类型
@router.get("/keyword/type")
@require_token('getListKeyWord,GET')
async def get_kewword_group_type(request: Request, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    group_by_type = await Crud.group_by(db=db, model=keyWord.type, _group_by=keyWord.type)
    return Success(data={'keywordType': jsonable_encoder(group_by_type)})


@router.get("/keywords/")
@require_token('getListKeyWord,GET')
async def get_kewword_list(request: Request, 
    background_task: BackgroundTasks,
    paging: Optional[int] = Query(1), 
    params: CommonQueryParams = Depends(), 
    type: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    start_end: Optional[str] = Query(None), 
    update_start_end: Optional[str] = Query(None), 
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db)
):


    filters = []
    # 判断是否有状态查询
    if status is not None:
        # setattr(params, 'status', status) 
        filters.append(keyWord.status == status)


    if type is not None:
            # setattr(params, 'status', status) 
            filters.append(keyWord.type == type)

    
   #  是否搜索创建时间
    if start_end:
        _start_end = start_end.split(',')
        if len(_start_end) == 2:
            filters.append(and_(keyWord.created_at >= _start_end[0], keyWord.created_at <= _start_end[1]))

   #  是否搜索更新时间
    if update_start_end:
        _update_start_end = update_start_end.split(',')
        if len(_update_start_end) == 2:
            filters.append(and_(keyWord.updated_at >= _update_start_end[0], keyWord.updated_at <= _update_start_end[1]))

    if params.keyword:
        filters.append(keyWord.name.like("%" + params.keyword + '%'))



    # 是否条件下载
    if not paging:
        path = str(uuid.uuid1())
        _field, _update = excelField()

        background_task.add_task(get_pro, path=path, task_name="关键词管理", current_user=current_user.username, filters=filters, model=keyWord, field=_field, update=_update)
        #get_pro(path=path, task_name="关键词管理", current_user=current_user.username, filters=filters, model=keyWord,field=_field, update=_update)
        return Success(data={'task_id': path }) 

    query, total = await Crud.get_items(db=db,model=keyWord, params=params,  other_filter=filters)
    # query, total = await Crud.get_items(db=db,model=keyWord, params=params, keyword_field='name', other_filter=filters)
    _list = jsonable_encoder(query)
    _total = total



    # 定义关键词查询状态
    keywordStatus = [{'label': '未查询', 'value': -2},  {'label': '正在查询','value': -1}, {'label': '已查询', 'value': 1}]
    data = {
        'list': _list,
        'totalCount': _total,
        'keywordStatus': keywordStatus,
    }
    return Success(data=data)


#  获取计划任务
@router.get("/batch/keyword/download")
@require_token('getListKeyWord,GET')
async def batch_download_keyword(request: Request, task_id: str = Query(...),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):


    _rdata,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path==task_id, taskRecord.first_name==current_user.username)])
    if _rdata:
        return Success(data={ "task": jsonable_encoder(_rdata[0])})
    else:
        return Success(data={ "task": {'progress': 0}})
 


# 条件更新
@router.post("/batch/keyword/update/condition")
@require_token('ConditionBatchUpdateKeyword,POST')
async def get_kewword_list(request: Request, 
    item: batchConditionUpdataKeyWordSchema,
    params: CommonQueryParams = Depends(), 
    type: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    start_end: Optional[str] = Query(None), 
    update_start_end: Optional[str] = Query(None), 
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db)
):


    filters = []
    # 判断是否有状态查询
    if status is not None:
        # setattr(params, 'status', status) 
        filters.append(keyWord.status == status)


    if type is not None:
            # setattr(params, 'status', status) 
            filters.append(keyWord.type == type)

    
   #  是否搜索创建时间
    if start_end:
        _start_end = start_end.split(',')
        if len(_start_end) == 2:
            filters.append(and_(keyWord.created_at >= _start_end[0], keyWord.created_at <= _start_end[1]))

   #  是否搜索更新时间
    if update_start_end:
        _update_start_end = update_start_end.split(',')
        if len(_update_start_end) == 2:
            filters.append(and_(keyWord.updated_at >= _update_start_end[0], keyWord.updated_at <= _update_start_end[1]))

    if params.keyword:
        filters.append(keyWord.name.like("%" + params.keyword + '%'))


    path = str(uuid.uuid1())
    get_pro(path=path, task_name="关键词管理条件更新", current_user=current_user.username, filters=filters, model=keyWord,  ConditionUpdate=True, oneField="status", oneValue=item.status)
    return Success(data={'task_id': path })

    return Success()











@router.get("/keyword/{id}")
@require_token('getKeyWord,GET')
async def get_kewword(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=keyWord, id=id)
    return Success(data=jsonable_encoder(query))
    

@router.post("/keyword")
@require_token('createKeyWord,POST')
async def create_keyword(request: Request, item: CreateKeyWordSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    is_keyword_exists,_ = await Crud.get_items(db=db, model=keyWord, other_filter=[keyWord.name==item.name])
    if is_keyword_exists:
        raise HTTPException(status_code=400, detail=f'{item.name} 已存在')

    query = await Crud.create_item(
            db=db, 
            model=keyWord, 
            name=item.name, 
            type=item.type,
            first_name=current_user.username,
    )
    return Success(data=jsonable_encoder(query))



@router.delete("/keyword/{id}")
@require_token('deleteKeyWord,DELETE')
async def del_keyword(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    

    # query = await Crud.show_item(db=db, model=keyWord, id=id)
    # 删除标签关联
    # query.searchkeywords = []

    await Crud.delele_item(db=db, model=keyWord, id=id)
    return Success()




@router.put("/keyword/{id}")
@require_token('modifyKeyWord,PUT')
async def update_keyword(request: Request, item: CreateKeyWordSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # 北京时间
    # _now = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=keyWord,
                name=item.name,
                type=item.type,
                updated_at=get_today(hms=True),
                status=item.status,
                last_name=current_user.username
            )
    return Success(data=jsonable_encoder(query))





@router.post("/batch/keyword")
@require_token('batchAddKeyWord,POST')
async def batch_create_keyword(request: Request, item: batchCreateKeyWordSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # print('test')

    # 判断是否有数据
    if  not item.batchContent:
        raise HTTPException(status_code=400, detail='无数据添加')

    value = []
    is_exists = []
    if isinstance(item.batchContent, str):
        # newbatchContent = []
        batchContent = item.batchContent.split('\n')
        for b in batchContent:
            if b:
                v = b.replace(' ', '')
                value.append(v)
                # newbatchContent.append({'name': v})

        
        # item.batchContent = newbatchContent
    

    # 搜索是否重复, 如果有重复，则保存到列表中，无重复则添加到数据库
    o, _ = await Crud.get_items(db=db,model=keyWord, paging=False, other_filter=[and_(keyWord.name.in_(value), keyWord.type==item.type)]) 

    # raise HTTPException(status_code=400, detail='error')
    if o:
        s = list(map(lambda x:x.name, o))
        is_exists = is_exists + s
        insert_db = list(set(value).difference(set(is_exists)))
        # raise HTTPException(status_code=400, detail=f'{",".join(s)} 已存在')
    else:
        insert_db = value

    newbatchContent = [] 
    for v in insert_db:
        newbatchContent.append({'name': v, 'type': item.type})
    
    _data = {'successTotal': len(insert_db), 'errorTotal': len(is_exists), 'errorData': is_exists}

    try:
        if newbatchContent:
            db.execute(keyWord.__table__.insert(), newbatchContent)
            db.commit()
        return Success(data=_data)
    except IntegrityError as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='存在重复数据,请过滤重复数据后再添加')
    except SQLAlchemyError as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='数据库繁忙,请稍后重新提交')
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='批量添加失败,请联系管理员')


# 批量删除

@router.post("/batch/keyword/delete")
@require_token('batchDeleteKeyWord,POST')
async def batch_delete_keyword(request: Request, item: batchDeleteKeyWordSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    await Crud.multi_delete(db=db, model=keyWord, ids=item.ids, multi_delete=True)
    return Success()


# 批量更新
@router.post("/batch/keyword/updata")
@require_token('batchUpdataKeyWord,POST')
async def batch_updata_keyword(request: Request, item: batchUpdataKeyWordSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    try:
        db.query(keyWord).filter(keyWord.id.in_(item.ids)).update({keyWord.status : item.status},  synchronize_session=False)
        db.commit()
        return Success()
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='更新状态失败')
    



# 随机分配关键词

@router.get("/random/keyword")
@require_token('randomKeyWord,GET')
async def random_keyword(request: Request, type: Union[str,None] = None, current_user: LoginCrud.verify_token = Depends(),   db: Session = Depends(get_db)):

    _type = '百度'
    if type and type.lower() == 'sogou' or type == '搜狗':
        _type = '搜狗'


    # 再返回当天用户的数据
    # _now = (datetime.now() + timedelta(hours=8))
    _startTime = get_today() + ' 00:00:00'
    _endTime = get_today() + ' 23:59:59'
    filters = [and_(searchKeyWord.first_name == current_user.username, searchKeyWord.created_at >= _startTime, searchKeyWord.created_at <= _endTime)]
    _, total = await Crud.get_items(db=db,model=searchKeyWord, paging=False, other_filter=filters)


    # 先查询用户是否已经分配关键词
    exists, _ = await Crud.get_items(db=db,model=keyWord, paging=False, other_filter=[and_(keyWord.search_user==current_user.username, keyWord.status==-1, keyWord.type==_type)])
    if exists:
        return Success(data={'next': exists[0].name, 'id': exists[0].id, 'total': total })



    query, _ = await Crud.get_items(db=db,model=keyWord, paging=False, other_filter=[and_(keyWord.status==-2, keyWord.type==_type)])
    if not query:
        raise HTTPException(status_code=400, detail='关键词已用完,请联系管理员, Thank You, Keyword used up, Please contact the administrator.')
    getOne = random.choice(query)

    # 北京时间
    
    getOne.status = -1
    getOne.updated_at = get_today(hms=True)
    getOne.search_user = current_user.username
    getOne.last_name = '系统自动更新'

    db.commit()


    return Success(data={'next': getOne.name, 'id': getOne.id, 'total': total })




