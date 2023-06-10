from fastapi import APIRouter,Depends,Request,HTTPException,Query,BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_,and_
from api.models import Weight, SearchWeight,User,taskRecord
from api.schemas import CreateSearchWeightSchema, BatchCreateSearchWeightSchema, LockSearchWeightSchema, batchDeleteSearchWeightSchema
from api.dependen import CommonQueryParams,get_db, require_token
from sqlalchemy.orm import Session
from api.services import LoginCrud,Crud
from sqlalchemy.exc import SQLAlchemyError
from api.utils import Success,logger,get_today
from typing import Optional
from .AdminWeight import WeightTypes
import uuid
from api.tasks import get_pro



router = APIRouter()


def excelField():
    _field = {
            "owner": "权重名称",
            "number": "排名序号", "link": "对应链接", 
            "url_website":"网站网址", "contact": "联系方式",
            "is_contact": "是否锁定", "contact_user": "联系人",
            "color": "颜色", "en": "英文",
            "description":"描述", 
            "first_name":"创建者", "last_name":"更新者",
            "created_at": "导入时间", "updated_at": "更新时间",
        }
    _update = {
            'is_contact': {"0": "未锁定",  "1": "已锁定"}, 
            'owner': ['name'], # 获取关联表中其中一个值，必须序列化数据也是列表或者字典
        }
    return _field, _update






@router.get("/searchweights/")
@require_token('getListSearchWeight,GET')
async def get_searchweight_list(request: Request, 
        background_task: BackgroundTasks,
        is_contact: Optional[int] = Query(None),
        type: Optional[str] = Query(None),
        paging: Optional[int] = Query(1), 
        asynckeyword: Optional[str] = Query(None), 
        lock: Optional[int] = Query(None),
        number: Optional[int] = Query(None),
        en: Optional[str] = Query(None),
        contact_user: Optional[str] = Query(None), 
        first_name: Optional[str] = Query(None), 
        last_name: Optional[str] = Query(None), 
        start_end: Optional[str] = Query(None), 
        update_start_end: Optional[str] = Query(None), 
        params: CommonQueryParams = Depends(),
        current_user: LoginCrud.verify_token = Depends(), 
        db: Session = Depends(get_db)
):

    filters = []

    # 是否排名
    if number:
        filters.append(SearchWeight.number==number)

    if en:
        filters.append(SearchWeight.en==en)

    # 是否搜索锁定
    if lock is not None:
        filters.append(SearchWeight.is_contact==lock)

    # 是否搜索执行者
    if contact_user:
        filters.append(SearchWeight.contact_user==contact_user)

    # 是否搜索导入者
    if first_name:
        filters.append(SearchWeight.first_name==first_name)


     # 是否搜索更新者
    if last_name:
        filters.append(SearchWeight.last_name==last_name)

    # 是否搜索联系方式
    if is_contact is not None:
        # print(is_contact)
        filters.append(SearchWeight.contact != '' ) if is_contact  else filters.append(SearchWeight.contact == '')
        # raise HTTPException(status_code=400, detail="test")

    #  是否搜索创建时间
    if start_end:
        _start_end = start_end.split(',')
        if len(_start_end) == 2:
            filters.append(and_(SearchWeight.created_at >= _start_end[0], SearchWeight.created_at <= _start_end[1]))

   #  是否搜索更新时间
    if update_start_end:
        _update_start_end = update_start_end.split(',')
        if len(_update_start_end) == 2:
            filters.append(and_(SearchWeight.updated_at >= _update_start_end[0], SearchWeight.updated_at <= _update_start_end[1]))

    # 是否搜索查询数据
    if asynckeyword:
        _asynck = asynckeyword.split(',') or list[asynckeyword]
        filters.append(SearchWeight.owner_id.in_(_asynck))


    # 是否搜索的库存
    join_model = None
    if type:
        join_model = Weight
        filters.append(Weight.type == type)

    
    if params.keyword:
        filters.append(or_(
            SearchWeight.link.like("%" + params.keyword + '%'),
            SearchWeight.url_website.like("%" + params.keyword + '%'),
            SearchWeight.contact.like("%" + params.keyword + '%'),
            SearchWeight.description.like("%" + params.keyword + '%'),
        ))

    # 是否条件下载
    if not paging:
        path = str(uuid.uuid1())
        _field, _update = excelField()

        # print(jsonable_encoder(query))
        background_task.add_task(get_pro, path=path, task_name="权重搜索条件下载", current_user=current_user.username, filters=filters, model=SearchWeight, join_model=join_model, field=_field, update=_update)
        #get_pro(path=path, task_name="权重搜索条件下载", current_user=current_user.username, filters=filters, model=SearchWeight, join_model=join_model, field=_field, update=_update)
        return Success(data={'task_id': path }) 


    query, total = await Crud.get_items(db=db,model=SearchWeight,join_model=join_model, params=params, other_filter=filters)
    # 获取所有数据, 默认已未锁定排列
    # order_field = [searchKeyWord.id,  searchKeyWord.owner_id, searchKeyWord.number.desc()]
    # query, total = await Crud.get_items(db=db,model=searchKeyWord, params=params, other_filter=filters,order_enable=True, order_field=searchKeyWord.id.desc())
    

    _list = jsonable_encoder(query)
    _total = total


    # 整合数据

    data = {
        'list': _list,
        'totalCount': _total,
    }
    return Success(data=data)

#  获取计划任务
@router.get("/batch/searchweights/download")
@require_token('getListSearchWeight,GET')
async def batch_download_keyword(request: Request, task_id: str = Query(...),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):


    _rdata,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path==task_id, taskRecord.first_name==current_user.username)])
    if _rdata:
        return Success(data={ "task": jsonable_encoder(_rdata[0])})
    else:
        return Success(data={ "task": {'progress': 0}})
 


# 获取所有序号
@router.get("/searchweights/groupby/number")
@require_token('getListSearchWeightNumber,GET')
async def get_searchweight_group_by_number(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    group_by_number = await Crud.group_by(db=db, model=SearchWeight.number, _group_by=SearchWeight.number)
    return Success(data={'numbers': jsonable_encoder(group_by_number)})


# 获取所有提交用户
@router.get("/searchweights/groupby/user")
@require_token('getListSearchWeightUser,GET')
async def get_searchweight_group_by_first_name(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    group_by_first_name = await Crud.group_by(db=db, model=SearchWeight.first_name, _group_by=SearchWeight.first_name)
    return Success(data={'first_names': jsonable_encoder(group_by_first_name)})



    
# 获取所有关键词标签
@router.get("/searchweights/groupby/en")
@require_token('getListSearchWeightEn,GET')
async def get_searchweight_group_by_ens(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    group_by_en = await Crud.group_by(db=db, model=SearchWeight.en, _group_by=SearchWeight.en)
    return Success(data={'ens': jsonable_encoder(group_by_en)})



# 只限权重搜索
@router.get("/searchweights/search/")
@require_token('getListSearchWeight,GET')
async def get_search_keyword(request: Request, q: Optional[str] = Query(None), s: Optional[int] = Query(None),params: CommonQueryParams = Depends(),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    if s and q:
        result, _ = await Crud.get_items(db=db, model=Weight,  params=params,other_filter=[and_(Weight.name.like("%" + q +"%"),Weight.status==1)])

    else:
       result, _ = await Crud.get_items(db=db, model=Weight,  params=params,other_filter=[Weight.name.like("%" + q +"%")]) 
    data = jsonable_encoder(result, include=['id', 'name'])
    return Success(data=data)


# 获取其他数据
@router.get("/searchweights/groupby")
@require_token('getListSearchWeightOther,GET')
async def get_searchweight_group_by(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # # # 获取所有关键词
    # k_query, _ = await Crud.get_items(db=db,model=Weight, paging=False) 
    # existSearchs = [ k for k in k_query if k.status == 1]



    # # 获取所有分组
    # # group_by_number = await Crud.group_by(db=db, model=SearchWeight.number, _group_by=SearchWeight.number)
    # group_by_is_contact= await Crud.group_by(db=db, model=SearchWeight.is_contact, _group_by=SearchWeight.is_contact)
    # group_by_contact_user = await Crud.group_by(db=db, model=SearchWeight.contact_user, _group_by=SearchWeight.contact_user)
    # # group_by_first_name = await Crud.group_by(db=db, model=SearchWeight.first_name, _group_by=SearchWeight.first_name)
    # group_by_last_name = await Crud.group_by(db=db, model=SearchWeight.last_name, _group_by=SearchWeight.last_name)
    # # group_by_en = await Crud.group_by(db=db, model=SearchWeight.en, _group_by=SearchWeight.en)
    # group_by_color = await Crud.group_by(db=db, model=SearchWeight.color, _group_by=SearchWeight.color)
    

    # new_group_by_is_contact = jsonable_encoder(group_by_is_contact)
    # for i in new_group_by_is_contact:
    #     if i['is_contact']:
    #         i['label'] = '已锁定'
    #     elif i['is_contact'] == 0:
    #         i['label'] = '未锁定'
    #     else:
    #         pass


    # 定义权重库存
    weightTypes = list(map(lambda x:x.value, WeightTypes))
    all_users,_ = await Crud.get_items(db=db, model=User, paging=False, other_filter=[User.status == 1])
    group_by_color = [{'color': '#67C23A'}, {'color': '#E6A23C'},{'color': '#F56C6C'}]
    group_by_is_contact = [{'label': '未锁定', 'is_contact': 0}, {'label': '已锁定', 'is_contact': 1}]
    ens = [{'en': "other"}, {'en': "sex"}, {'en': "wrong"}]
    is_contacts = [{'label': "无", 'value': 0 }, {'label': "有", 'value': 1 }]


    _all_users =  jsonable_encoder(all_users)
    # _keywords = jsonable_encoder(k_query, include=['id', 'name', 'status'])
    data = {
        # 'existSearchs': _keywords,
        # 'keywords': _keywords,
        'first_names': _all_users,
        'last_names': _all_users,
        'contact_users': _all_users,
        'is_locks': group_by_is_contact,
        'colors': group_by_color,
        'ens': ens,
        "weightypes": weightTypes,
        "is_contacts": is_contacts
    }
    # data = {
    #     'existSearchs': jsonable_encoder(existSearchs),
    #     'keywords': jsonable_encoder(k_query, include=['id', 'name', 'status']),
    #     # 'first_names': jsonable_encoder(group_by_first_name),
    #     'last_names': jsonable_encoder(group_by_last_name),
    #     'contact_users': jsonable_encoder(group_by_contact_user),
    #     'is_locks': jsonable_encoder(new_group_by_is_contact),
    #     # 'numbers': jsonable_encoder(group_by_number),
    #     # 'ens': jsonable_encoder(group_by_en),
    #     'colors': jsonable_encoder(group_by_color)
        
    # }



    return Success(data=data)




@router.get("/searchweight/{id}")
@require_token('getSearchWeight,GET')
async def get_searchweight(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=SearchWeight, id=id)
    return Success(data=jsonable_encoder(query))
    



@router.post("/searchweight")
@require_token('createSearchWeight,POST')
async def create_searchweight(request: Request, item: CreateSearchWeightSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    # 先查询是否存在关键词ID
    kq =  await Crud.show_item(db=db, model=Weight, id=item.owner_id)
    kq.status = 1
    



    # quan
    query = await Crud.create_item(
            db=db, 
            model=SearchWeight, 
            # number=item.number, 
            link=item.link, 
            url_website=item.url_website, 
            contact=item.contact, 
            cn=item.cn, 
            en=item.en, 
            color=item.color, 
            owner_id=item.owner_id,
            first_name=current_user.username,
            description=item.description
    )
    return Success(data=jsonable_encoder(query))



@router.delete("/searchweight/{id}")
@require_token('deleteSearchWeight,DELETE')
async def del_searchweight(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    

    # query = await Crud.show_item(db=db, model=keyWord, id=id)
    # 删除标签关联
    # query.searchkeywords = []

    await Crud.delele_item(db=db, model=SearchWeight, id=id)
    return Success()




@router.put("/searchweight/{id}")
@require_token('modifySearchWeight,PUT')
async def update_searchweight(request: Request, item: CreateSearchWeightSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # 先查询是否存在关键词ID
    await Crud.show_item(db=db, model=Weight, id=item.owner_id)

    # 北京时间

    query = await Crud.update_item(
                db=db, 
                id=id,
                model=SearchWeight,
                owner_id=item.owner_id,
                # number=item.number, 
                link=item.link, 
                url_website=item.url_website, 
                contact=item.contact, 
                cn=item.cn, 
                en=item.en, 
                color=item.color, 
                updated_at=get_today(hms=True),
                last_name=current_user.username,
                description=item.description
            )
    return Success(data=jsonable_encoder(query))


# 锁定某个关键词下的网址
@router.put("/searchweight/{id}/lock")
@require_token('lockSearchWeight,PUT')
async def lock_searchweight(request: Request, item: LockSearchWeightSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):


    # 锁定
    query = await Crud.show_item(db=db, model=SearchWeight, id=id)
    query.is_contact = item.is_contact
    if item.is_contact:
        query.contact_user = current_user.username
        query.last_name = current_user.username
        query.updated_at=get_today(hms=True)
    else:
        query.contact_user = ''
        query.last_name = current_user.username
        query.updated_at=get_today(hms=True)
    

        
    

    # 修改 keyword 状态
    # k = await Crud.show_item(db=db, model=keyWord, id=query.owner_id)
    # k.status = 1

    db.commit()
    return Success()



 

@router.post("/batch/searchweight")
@require_token('batchAddSearchWeight,POST')
async def create_searchweight(request: Request, item: BatchCreateSearchWeightSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):



    body_data = item.data
    for b in body_data:
        owner_id = b.get('owner_id',None)
        number = b.get('number',None)
        link = b.get('link',None)
        url_website = b.get('url_website',None)
        contact = b.get('contact',None)
        cn = b.get('cn',None)
        en = b.get('en',None)
        color = b.get('color',None)
        if not owner_id  or not link:
            raise HTTPException(status_code=400, detail='无效数据;invalid data') 

        b['owner_id'] =owner_id
        b['number'] = number
        b['first_name'] = current_user.username
        b['cn'] = cn
        b['en'] = en
        b['color'] = color
        b['updated_at'] = get_today(hms=True)


    # 返回它当天提交的数据
    _startTime = get_today() + ' 00:00:00'
    _endTime = get_today() + ' 23:59:59'


    try:
        db.execute(
            SearchWeight.__table__.insert(body_data)
        )



        db.query(Weight).filter(and_(Weight.status==-1, Weight.search_user == current_user.username)).update({ Weight.status : 1, Weight.updated_at : get_today(hms=True) }, synchronize_session=False)
        # g = db.query(Weight).filter(and_(Weight.status==-1, Weight.search_user == current_user.username)).all()
        db.commit()

        filters = [and_(SearchWeight.first_name == current_user.username, SearchWeight.created_at >= _startTime, SearchWeight.created_at <= _endTime)]
        _, total = await Crud.get_items(db=db,model=SearchWeight, paging=False, other_filter=filters)
        return Success(data={'total': total})
    except SQLAlchemyError as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='数据库繁忙,请稍后重新提交')
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='批量添加失败,请联系管理员')







@router.post("/batch/searchweight/delete")
@require_token('batchDeleteSearchWeight,POST')
async def batch_delete_weight(request: Request, item: batchDeleteSearchWeightSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    await Crud.multi_delete(db=db, model=SearchWeight, ids=item.ids, multi_delete=True)
    return Success()





@router.post("/batch/searchweight/lock")
@require_token('handleBatchLockWeight,POST')
async def batch_lock_weight(request: Request, item: batchDeleteSearchWeightSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    # 北京时间

    try:
        query,_ = await Crud.get_items(db=db, model=SearchWeight, paging=False, other_filter=[SearchWeight.id.in_(item.ids)])
        for q in query:

            # 如果不是超级管理员，并且已经锁定，但是不是自己锁定
            if not current_user.is_super and q.is_contact and q.contact_user != current_user.username:
                raise HTTPException(status_code=400, detail='不允许修改其他用户的锁定，谢谢谅解')
            

            q.is_contact = 1
            q.contact_user = current_user.username
            q.last_name = current_user.username
            q.updated_at=get_today(hms=True)

        db.commit()
        
        return Success()
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='修改失败')
    except Exception as e:
        raise HTTPException(status_code=500, detail='请联系超级管理员')


