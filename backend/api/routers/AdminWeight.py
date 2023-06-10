from datetime import datetime, timedelta
import uuid
from fastapi import APIRouter,Depends,Request,Query,HTTPException,BackgroundTasks, Body
from fastapi.encoders import jsonable_encoder
from api.models import Weight,SearchWeight, taskRecord
from api.schemas import CreateWeightSchema, batchCreateWeightSchema, batchDeleteWeightSchema, batchUpdataWeightSchema, batchConditionUpdataWeightSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud
from sqlalchemy.orm import Session 
from api.utils.response import Success
from api.services import LoginCrud
from typing import Optional,Union
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from api.utils import logger,get_today,get_domain
import random
from sqlalchemy import and_
from enum import Enum, unique
from api.dependen.lockRedis import lock
from api.exts import Schedule
from api.tasks import batch_add,get_pro
import uuid



router = APIRouter()



@unique
class WeightTypes(Enum):
    one_db = '总库存'
    two_db = '二次筛选'


@unique
class WeighSearchtEns(Enum):
    sex = 'sex'
    wrong = 'wrong'
    other = 'other'
    movie = 'movie'


def excelField():
    _field = {
            'name': "权重域名", "type": "库存类型", 
            "created_at": "导入时间", "updated_at": "更新时间", 
            "first_name":"导入人", "status": "域名类型", 
            "search_user":"搜索人", "last_name":"更新人",
            "searchweights": "域名分类"
        }
    _update = {
            'status': {"-2": "未查询", "-1": "正在查询", "1": "已查询"}, 
            'searchweights': ['en'], # 获取关联表中其中一个值，必须序列化数据也是列表
        }
    return _field, _update


# def batch_add(content,_type, db):
#     if isinstance(content, str):
#         batchContent = content.split('\n')
#         for b in batchContent:
#             if b:
#                 name = get_domain(b)
#                 # o, _ = await Crud.get_items(db=db, model=Weight, paging=False, other_filter=[Weight.name==name])
#                 o = db.query(Weight).filter(and_(Weight.name==name, Weight.type==_type)).first()
#                 if not o:
#                     obj = Weight(name=name, type=_type)
#                     db.add(obj)
#                     db.commit()
#                     db.refresh(obj)
                    




@router.get("/weights/")
@require_token('getListWeight,GET')
async def get_weight_list(request: Request, 
    background_task: BackgroundTasks,
    paging: Optional[int] = Query(1), 
    params: CommonQueryParams = Depends(), 
    status: Optional[int] = Query(None),
    type: Optional[str] = Query(None), 
    en: Optional[str] = Query(None), 
    start_end: Optional[str] = Query(None), 
    update_start_end: Optional[str] = Query(None), 
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db),
    
):

    filters = []
    # 判断是否有状态查询
    if status is not None:
        # setattr(params, 'status', status) 
        filters.append(Weight.status == status)

    if params.keyword:
        filters.append(Weight.name.like("%" + params.keyword + "%"))
    
   #  是否搜索创建时间
    if start_end:
        _start_end = start_end.split(',')
        if len(_start_end) == 2:
            filters.append(and_(Weight.created_at >= _start_end[0], Weight.created_at <= _start_end[1]))

   #  是否搜索更新时间
    if update_start_end:
        _update_start_end = update_start_end.split(',')
        if len(_update_start_end) == 2:
            filters.append(and_(Weight.updated_at >= _update_start_end[0], Weight.updated_at <= _update_start_end[1]))


    # 是否搜索的权重库存
    if type:
        filters.append(Weight.type == type)

    join_model = None
    if en:
        join_model = SearchWeight
        filters.append(SearchWeight.en == en)
        
    
    # 是否条件删除
    path = str(uuid.uuid1())

    
    # 是否条件下载
    if not paging:
        _field, _update = excelField()

        # print(jsonable_encoder(query))
        background_task.add_task(get_pro, path=path, task_name="权重管理条件下载", current_user=current_user.username, filters=filters, model=Weight, join_model=join_model, field=_field, update=_update)
        # get_pro(path=path, task_name="权重管理", current_user=current_user.username, filters=filters, model=Weight, join_model=join_model, field=_field, update=_update)
        return Success(data={'task_id': path }) 
        

    # 获取默认数据
    query, total = await Crud.get_items(db=db,model=Weight, join_model=join_model, params=params, other_filter=filters)

    # 定义关键词查询状态
    keywordStatus = [{'label': '未查询', 'value': -2},  {'label': '正在查询','value': -1}, {'label': '已查询', 'value': 1}]


    # 定义权重库存
    weightTypes = list(map(lambda x:x.value, WeightTypes))

    # 定义域名类型
    ens = list(map(lambda x:x.value, WeighSearchtEns))


    # if en:
    #     data = {
    #         'list': jsonable_encoder(new_list),
    #         'totalCount': len(new_list),
    #         'keywordStatus': keywordStatus,
    #         'weightTypes': weightTypes,
    #         'ens' : ens,
    #     }
    # else:
    data = {
        'list': jsonable_encoder(query),
        'totalCount': total,
        'keywordStatus': keywordStatus,
        'weightTypes': weightTypes,
        'ens' : ens,
    }

    # 是否搜索的是权重域名类别
    # new_list = []
    # if en:
    #     for i in _list:
    #         if i.get('searchweights', []) and i.get('searchweights', [])[0]['en'] == en:
    #             new_list.append(i)
    #     data['list'] = new_list


    
    return Success(data=data)

# 条件删除
@router.post("/batch/weight/delete/condition")
@require_token('ConditionBatchDeleteWeigh,POST')
async def get_weight_list(request: Request, 
    background_task: BackgroundTasks,
    params: CommonQueryParams = Depends(), 
    status: Optional[int] = Query(None),
    type: Optional[str] = Query(None), 
    en: Optional[str] = Query(None), 
    start_end: Optional[str] = Query(None), 
    update_start_end: Optional[str] = Query(None), 
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db),
    
):


    filters = []
    # 判断是否有状态查询
    if status is not None:
        # setattr(params, 'status', status) 
        filters.append(Weight.status == status)

    if params.keyword:
        filters.append(Weight.name.like("%" + params.keyword + "%"))
    
   #  是否搜索创建时间
    if start_end:
        _start_end = start_end.split(',')
        if len(_start_end) == 2:
            filters.append(and_(Weight.created_at >= _start_end[0], Weight.created_at <= _start_end[1]))

   #  是否搜索更新时间
    if update_start_end:
        _update_start_end = update_start_end.split(',')
        if len(_update_start_end) == 2:
            filters.append(and_(Weight.updated_at >= _update_start_end[0], Weight.updated_at <= _update_start_end[1]))


    # 是否搜索的权重库存
    # if type:
    filters.append(Weight.type == "二次筛选")

    join_model = None
    if en:
        join_model = SearchWeight
        filters.append(SearchWeight.en == en)
        
    

    path = str(uuid.uuid1())
    #get_pro(path=path, task_name="权重管理条件删除", current_user=current_user.username, filters=filters, model=Weight, join_model=join_model, ConditionDelete=True)
    background_task.add_task(get_pro, path=path, task_name="权重管理条件删除", current_user=current_user.username, filters=filters, model=Weight, join_model=join_model, ConditionDelete=True)
    return Success(data={'task_id': path })
    

# 条件更新
@router.post("/batch/weight/update/condition")
@require_token('ConditionBatchUpdateWeigh,POST')
async def get_weight_list(request: Request,
    background_task: BackgroundTasks,
    item: batchConditionUpdataWeightSchema,
    params: CommonQueryParams = Depends(), 
    status: Optional[int] = Query(None),
    type: Optional[str] = Query(None), 
    en: Optional[str] = Query(None), 
    start_end: Optional[str] = Query(None), 
    update_start_end: Optional[str] = Query(None), 
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db),
    
    
):


    filters = []
    # 判断是否有状态查询
    if status is not None:
        # setattr(params, 'status', status) 
        filters.append(Weight.status == status)

    if params.keyword:
        filters.append(Weight.name.like("%" + params.keyword + "%"))
    
   #  是否搜索创建时间
    if start_end:
        _start_end = start_end.split(',')
        if len(_start_end) == 2:
            filters.append(and_(Weight.created_at >= _start_end[0], Weight.created_at <= _start_end[1]))

   #  是否搜索更新时间
    if update_start_end:
        _update_start_end = update_start_end.split(',')
        if len(_update_start_end) == 2:
            filters.append(and_(Weight.updated_at >= _update_start_end[0], Weight.updated_at <= _update_start_end[1]))


    # 是否搜索的权重库存
    if type:
        filters.append(Weight.type == type)

    join_model = None
    if en:
        join_model = SearchWeight
        filters.append(SearchWeight.en == en)
        
    

    path = str(uuid.uuid1())
    # get_pro(path=path, task_name="权重管理条件更新", current_user=current_user.username, filters=filters, model=Weight, join_model=join_model, ConditionUpdate=True, oneField="status", oneValue=item.status)
    background_task.add_task(get_pro, path=path, task_name="权重管理条件更新", current_user=current_user.username, filters=filters, model=Weight, join_model=join_model, ConditionUpdate=True, oneField="status", oneValue=item.status)
    return Success(data={'task_id': path })



@router.get("/weight/{id}")
@require_token('getWeight,GET')
async def get_weight(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=Weight, id=id)
    return Success(data=jsonable_encoder(query))
    

@router.post("/weight")
@require_token('createWeight,POST')
async def create_weight(request: Request, item: CreateWeightSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    name = get_domain(item.name)

    # print(name)
    # 查询是否已经存在
    _a,_ = await Crud.get_items(db=db, model=Weight, other_filter=[and_(Weight.name==name, Weight.type==item.type)])
    if _a:
        raise HTTPException(status_code=400, detail=f'顶级域名 {name} 已存在')
    
    
    query = await Crud.create_item(
            db=db, 
            model=Weight, 
            name=name, 
            type=item.type,
            first_name=current_user.username,
    )
    return Success(data=jsonable_encoder(query))


# 删除
@router.delete("/weight/{id}")
@require_token('deleteWeight,DELETE')
async def del_weight(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    

    # query = await Crud.show_item(db=db, model=keyWord, id=id)
    # 删除标签关联
    # query.searchkeywords = []

    await Crud.delele_item(db=db, model=Weight, id=id)
    return Success()



# 4000004728.com
@router.put("/weight/{id}")
@require_token('modifyWeight,PUT')
async def update_weight(request: Request, item: CreateWeightSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    name = get_domain(item.name)

    # print(name)
    # 假如名字已经存在，并且 ID 不是已经存在数据的 ID，返回错误
    _a,_ = await Crud.get_items(db=db, model=Weight, other_filter=[and_(Weight.name==name, Weight.type==item.type)])
    if _a and _a[0].id != id:
        raise HTTPException(status_code=400, detail=f' 顶级域名 {name} 已经存在')
    


    # 北京时间
    _now = get_today(hms=True)
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=Weight,
                name=name,
                type=item.type,
                updated_at=_now,
                status=item.status,
                last_name=current_user.username
            )
    return Success(data=jsonable_encoder(query))



# 批量添加

@router.post("/batch/weight")
@require_token('batchAddWeight,POST')
@lock('batch_add_weight')
async def batch_create_weight(request: Request, item: batchCreateWeightSchema,  current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(
get_db)):

    # 判断是否有数据
    if  not item.batchContent:
        raise HTTPException(status_code=400, detail='无数据添加')

    before = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    _path = request.scope['path']
    _uuid = uuid.uuid1().hex
    path = f'{_path}_{_uuid}'

    # 批量导入前 5 分钟查询是否存在有人提交了任务
    is_exist_task,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path.like(_path + "%"), taskRecord.progress != 100, taskRecord.created_at > before)])
    if is_exist_task:
        raise HTTPException(status_code=400, detail=f"{is_exist_task[0].created_at} {is_exist_task[0].first_name} 任务进度 {int(is_exist_task[0].progress)}% 正在运行中 , 请等任务完成后或者5分钟后再次提交")

    # batch_add(path,  item.batchContent, item.batchType, current_user.username)
    # 当前时间的后 10 秒执行导入
    next_cmd = (datetime.now() + timedelta(seconds=5)).strftime("%Y-%m-%d %H:%M:%S")
    Schedule.add_job(batch_add, 'date',  run_date=next_cmd, misfire_grace_time=3600, args=[path,  item.batchContent, item.batchType, current_user.username])

    return Success(data={'task_id': path })


#  获取计划任务
@router.get("/batch/weight")
@require_token('batchAddWeight,POST')
async def batch_import_caijin(request: Request, task_id: str = Query(...),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):


    _rdata,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path==task_id, taskRecord.first_name==current_user.username)])
    if _rdata:
        return Success(data={ "task": jsonable_encoder(_rdata[0])})
    else:
        return Success(data={ "task": {'progress': 0}})
 



# 批量删除

@router.post("/batch/weight/delete")
@require_token('batchDeleteWeight,POST')
async def batch_delete_weight(request: Request, item: batchDeleteWeightSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    await Crud.multi_delete(db=db, model=Weight, ids=item.ids, multi_delete=True)
    return Success()



# 批量更新
@router.post("/batch/weight/updata")
@require_token('batchUpdataWeight,POST')
async def batch_updata_keyword(request: Request, item: batchUpdataWeightSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    try:
        db.query(Weight).filter(Weight.id.in_(item.ids)).update({Weight.status : item.status},  synchronize_session=False)
        db.commit()
        return Success()
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='更新状态失败')
    


# 随机分配

@router.get("/random/weight")
@require_token('randomWeight,GET')
async def random_weight(request: Request,params: CommonQueryParams = Depends(), type: Optional[str] = None, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    if type and getattr(WeightTypes, type,  None):
        type = getattr(WeightTypes, type).value
    else:
        type = WeightTypes.one_db.value


    # 再返回当天用户的数据
    _startTime = get_today() + ' 00:00:00'
    _endTime = get_today() + ' 23:59:59'
    filters = [and_(SearchWeight.first_name == current_user.username, SearchWeight.created_at >= _startTime, SearchWeight.created_at <= _endTime)]
    _, total = await Crud.get_items(db=db,model=SearchWeight, paging=False, other_filter=filters)



    # 先查询用户是否已经分配关键词
    exists, _ = await Crud.get_items(db=db,model=Weight, paging=False, other_filter=[and_(Weight.search_user==current_user.username, Weight.status==-1, Weight.type==type)])
    if exists:
        return Success(data={'next': jsonable_encoder(exists, include=['id', 'name']), 'total': total })

    # 设置分页 30 条数据
    setattr(params, 'limit', 30) 
    query, _c = await Crud.get_items(db=db,model=Weight, params=params, other_filter=[and_(Weight.status==-2, Weight.type==type)])
    if not query:
        raise HTTPException(status_code=400, detail='权重域名已用完,请联系管理员, Thank You, Weighted domain name, Please contact the administrator.')
    
    # 随机分配一个，  random.sample(list, 5)  随机分配5个
    # getOne = random.choice(query)

    if len(query) > 10:
        getMany = random.sample(query, 10)
    else:
        getMany = query


    next = jsonable_encoder(getMany,include=['id', 'name'])


    # 北京时间
    for m in getMany:
        m.status = -1
        m.updated_at = get_today(hms=True)
        m.search_user = current_user.username
        m.last_name = '系统自动更新'

    db.commit()

    return Success(data={'next': next, 'total': total })