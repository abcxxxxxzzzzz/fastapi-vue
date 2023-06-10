from fastapi import APIRouter,Depends,Request,HTTPException,Query,BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_,and_
from api.models import searchKeyWord,keyWord,User,taskRecord
from api.schemas import CreateSearchKeyWordSchema,BatchCreateSearchKeyWordSchema,LockSearchKeyWordSchema,batchDeleteSearchKeyWordSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud
from sqlalchemy.orm import Session
from api.services import LoginCrud
from sqlalchemy.exc import SQLAlchemyError
from api.utils import logger,get_today,Success
from typing import Optional
import uuid
from api.tasks import get_pro

router = APIRouter()


def excelField():
    _field = {
            "type": "库存", "owner": "关键词名称",
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


@router.get("/searchkeywords/")
@require_token('getListSearchKeyWord,GET')
async def get_searchkeyword_list(request: Request, 
        background_task: BackgroundTasks,
        is_contact: Optional[int] = Query(None),
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
        type: Optional[str] = Query(None), 
        params: CommonQueryParams = Depends(),
        current_user: LoginCrud.verify_token = Depends(), 
        db: Session = Depends(get_db)
):

    filters = []

    # 是否词汇
    if type:
        filters.append(searchKeyWord.type==type)

    # 是否排名
    if number:
        filters.append(searchKeyWord.number==number)

    if en:
        filters.append(searchKeyWord.en==en)

    # 是否搜索锁定
    if lock is not None:
        filters.append(searchKeyWord.is_contact==lock)

    # 是否搜索执行者
    if contact_user:
        filters.append(searchKeyWord.contact_user==contact_user)

    # 是否搜索导入者
    if first_name:
        filters.append(searchKeyWord.first_name==first_name)


     # 是否搜索更新者
    if last_name:
        filters.append(searchKeyWord.last_name==last_name)

    # 是否搜索联系方式
    if is_contact is not None:
        # print(is_contact)
        filters.append(searchKeyWord.contact != '' ) if is_contact  else filters.append(searchKeyWord.contact == '')
        # raise HTTPException(status_code=400, detail="test")



    #  是否搜索创建时间
    if start_end:
        _start_end = start_end.split(',')
        if len(_start_end) == 2:
            filters.append(and_(searchKeyWord.created_at >= _start_end[0], searchKeyWord.created_at <= _start_end[1]))

   #  是否搜索更新时间
    if update_start_end:
        _update_start_end = update_start_end.split(',')
        if len(_update_start_end) == 2:
            filters.append(and_(searchKeyWord.updated_at >= _update_start_end[0], searchKeyWord.updated_at <= _update_start_end[1]))

    # 是否搜索查询数据
    if asynckeyword:
        _asynck = asynckeyword.split(',') or list[asynckeyword]
        filters.append(searchKeyWord.owner_id.in_(_asynck))
    
    if params.keyword:
        filters.append(or_(
            searchKeyWord.link.like("%" + params.keyword + '%'),
            searchKeyWord.url_website.like("%" + params.keyword + '%'),
            searchKeyWord.contact.like("%" + params.keyword + '%'),
            searchKeyWord.description.like("%" + params.keyword + '%'),
        ))

    # 是否条件下载
    if not paging:
        path = str(uuid.uuid1())
        _field, _update = excelField()

        background_task.add_task(get_pro, path=path, task_name="关键词搜索条件下载", current_user=current_user.username, filters=filters, model=searchKeyWord, field=_field, update=_update)
        # get_pro(path=path, task_name="关键词搜索条件下载", current_user=current_user.username, filters=filters, model=searchKeyWord, field=_field, update=_update)
        return Success(data={'task_id': path }) 

    query, total = await Crud.get_items(db=db,model=searchKeyWord, params=params, other_filter=filters)
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
@router.get("/batch/searchkeywords/download")
@require_token('getListSearchKeyWord,GET')
async def batch_download_keyword(request: Request, task_id: str = Query(...),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):


    _rdata,_ = await Crud.get_items(db=db, model=taskRecord, other_filter=[and_(taskRecord.path==task_id, taskRecord.first_name==current_user.username)])
    if _rdata:
        return Success(data={ "task": jsonable_encoder(_rdata[0])})
    else:
        return Success(data={ "task": {'progress': 0}})
 

# 获取所有序号
@router.get("/searchkeywords/groupby/number")
@require_token('getListSearchKeyWord,GET')
async def get_searchkeyword_group_by_number(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    group_by_number = await Crud.group_by(db=db, model=searchKeyWord.number, _group_by=searchKeyWord.number)
    return Success(data={'numbers': jsonable_encoder(group_by_number)})


# 获取所有提交用户
@router.get("/searchkeywords/groupby/user")
@require_token('getListSearchKeyWord,GET')
async def get_searchkeyword_group_by_first_name(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    group_by_first_name = await Crud.group_by(db=db, model=searchKeyWord.first_name, _group_by=searchKeyWord.first_name)
    return Success(data={'first_names': jsonable_encoder(group_by_first_name)})


    
# 获取所有关键词标签
@router.get("/searchkeywords/groupby/en")
@require_token('getListSearchKeyWord,GET')
async def get_searchkeyword_group_by_ens(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    group_by_en = await Crud.group_by(db=db, model=searchKeyWord.en, _group_by=searchKeyWord.en)
    return Success(data={'ens': jsonable_encoder(group_by_en)})



# 只限关键词搜索
@router.get("/searchkeywords/search/")
@require_token('getListSearchKeyWord,GET')
async def get_search_keyword(request: Request, q: Optional[str] = Query(None), s: Optional[int] = Query(None),params: CommonQueryParams = Depends(),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    if s and q:
        result, _ = await Crud.get_items(db=db, model=keyWord,  params=params,other_filter=[and_(keyWord.name.like("%" + q +"%"),keyWord.status==1)])

    else:
       result, _ = await Crud.get_items(db=db, model=keyWord,  params=params,other_filter=[keyWord.name.like("%" + q +"%")]) 
    data = jsonable_encoder(result, include=['id', 'name'])
    return Success(data=data)


@router.get("/searchkeywords/groupby")
@require_token('getListSearchKeyWord,GET')
async def get_searchkeyword_group_by(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    all_users,_ = await Crud.get_items(db=db, model=User, paging=False, other_filter=[User.status == 1])
    

    group_by_type = ['百度','搜狗']
    group_by_color = [{'color': '#67C23A'}, {'color': '#E6A23C'},{'color': '#F56C6C'}, {'color': '#87CEFA'}]
    group_by_is_contact = [{'label': '未锁定', 'is_contact': 0}, {'label': '已锁定', 'is_contact': 1}]
    ens = [{'en': "other"}, {'en': "sex"}, {'en': "wrong"}, {'en': "movie"}]
    is_contacts = [{'label': "无", 'value': 0 }, {'label': "有", 'value': 1 }]


    _all_users =  jsonable_encoder(all_users)
    # _keywords = jsonable_encoder(k_query, include=['id', 'name', 'status'])
    data = {
        # 'existSearchs': _keywords,
        # 'keywords': _keywords,
        'types': group_by_type,
        'first_names': _all_users,
        'last_names': _all_users,
        'contact_users': _all_users,
        'is_locks': group_by_is_contact,
        'colors': group_by_color,
        'ens': ens,
        "is_contacts": is_contacts
    }



    # all_users,_ = await Crud.get_items(db=db, model=User, paging=False, other_filter=[User.status == 1])
    # group_by_number = [{'number': 1}, {'number': 2}, {'number': 3}, {'number': 4}, {'number': 5}, {'number': 6}, {'number': 7}, {'number': 8}, {'number': 9}, {'number': 10}]



    # data = {
    #     'existSearchs': jsonable_encoder(existSearchs),
    #     'keywords': jsonable_encoder(k_query, include=['id', 'name', 'status']),
    #     # 'first_names': jsonable_encoder(group_by_first_name),
    #     # 'last_names': jsonable_encoder(group_by_last_name),
    #     # 'contact_users': jsonable_encoder(group_by_contact_user),
    #     'is_locks': group_by_is_contact,
    #     'numbers': group_by_number,
    #     'ens': group_by_en,
    #     'users': jsonable_encoder(all_users, include=['id', 'username']),
    # }
    return Success(data=data)




@router.get("/searchkeyword/{id}")
@require_token('getSearchKeyWord,GET')
async def get_searchkeyword(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=searchKeyWord, id=id)
    return Success(data=jsonable_encoder(query))
    



@router.post("/searchkeyword")
@require_token('createSearchKeyWord,POST')
async def create_searchkeyword(request: Request, item: CreateSearchKeyWordSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    

    #先查询是否存在关键词ID
    kq =  await Crud.show_item(db=db, model=keyWord, id=item.owner_id)
    kq.status = 1
    
    query = await Crud.create_item(
            db=db, 
            model=searchKeyWord, 
            number=item.number, 
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



@router.delete("/searchkeyword/{id}")
@require_token('deleteSearchKeyWord,DELETE')
async def del_searchkeyword(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    

    # query = await Crud.show_item(db=db, model=keyWord, id=id)
    # 删除标签关联
    # query.searchkeywords = []

    await Crud.delele_item(db=db, model=searchKeyWord, id=id)
    return Success()




@router.put("/searchkeyword/{id}")
@require_token('modifySearchKeyWord,PUT')
async def update_searchkeyword(request: Request, item: CreateSearchKeyWordSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # 先查询是否存在关键词ID
    await Crud.show_item(db=db, model=keyWord, id=item.owner_id)

    # 北京时间
    # _now = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

    query = await Crud.update_item(
                db=db, 
                id=id,
                model=searchKeyWord,
                owner_id=item.owner_id,
                number=item.number, 
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
@router.put("/searchkeyword/{id}/lock")
@require_token('lockSearchKeyWord,PUT')
async def lock_searchkeyword(request: Request, item: LockSearchKeyWordSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # 北京时间
    _now = get_today(hms=True)

    # 锁定
    query = await Crud.show_item(db=db, model=searchKeyWord, id=id)
    query.is_contact = item.is_contact
    if item.is_contact:
        query.contact_user = current_user.username
        query.last_name = current_user.username
        query.updated_at=_now
    else:
        query.contact_user = ''
        query.last_name = current_user.username
        query.updated_at=_now
    

        
    

    # 修改 keyword 状态
    # k = await Crud.show_item(db=db, model=keyWord, id=query.owner_id)
    # k.status = 1

    db.commit()
    return Success()





@router.post("/batch/searchkeyword")
@require_token('batchAddSearchKeyWord,POST')
async def create_searchkeyword(request: Request, item: BatchCreateSearchKeyWordSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    

    # print(item.data)
    # raise HTTPException(status_code=400, detail='正在维护中，请稍等再提交，等通知; It is under maintenance, please wait a moment before submitting it, and wait for the notice')
    # 北京时间
    # _now = (datetime.now() + timedelta(hours=8))


    body_data = item.data
    for b in body_data:
        owner_id = b.get('owner_id',None)
        number = b.get('number',None)
        cn = b.get('cn',None)
        en = b.get('en',None)
        color = b.get('color',None)
        _type = b.get('type', None)

        if _type and _type.lower() == 'sogou':
            b['type'] = '搜狗'
        elif _type and _type.lower() == 'baidu':
            b['type'] = '百度'
        else:
            pass

        b['owner_id'] =owner_id
        b['number'] = number
        b['first_name'] = current_user.username
        b['cn'] = cn
        b['en'] = en
        b['color'] = color
        b['created_at'] = get_today(hms=True)

        


    # 返回它当天提交的数据
    # _now = (datetime.now() + timedelta(hours=8))
    _startTime = get_today() + ' 00:00:00'
    _endTime = get_today() + ' 23:59:59'


    g = await Crud.show_item(db=db, model=keyWord, id=int(item.owner_id))
    if g.status == 1:
        raise HTTPException(status_code=200, detail=f'{g.name} 已提交过,请不要重复提交! This keyword has been submitted, please don\'t submit it again！')

    try:
        db.execute(
            searchKeyWord.__table__.insert(body_data)
        )
        g.status = 1
        g.updated_at = get_today(hms=True)
        db.commit()

        filters = [and_(searchKeyWord.first_name == current_user.username, searchKeyWord.created_at >= _startTime, searchKeyWord.created_at <= _endTime)]
        _, total = await Crud.get_items(db=db,model=searchKeyWord, paging=False, other_filter=filters)
        return Success(data={'total': total})
    except SQLAlchemyError as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='数据库繁忙,请稍后重新提交')
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail='批量添加失败,请联系管理员')







@router.post("/batch/searchkeyword/delete")
@require_token('batchDeleteSearchKeyWord,POST')
async def batch_delete_keyword(request: Request, item: batchDeleteSearchKeyWordSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    await Crud.multi_delete(db=db, model=searchKeyWord, ids=item.ids, multi_delete=True)
    return Success()





@router.post("/batch/searchkeyword/lock")
@require_token('handleBatchLock,POST')
async def batch_lock_keyword(request: Request, item: batchDeleteSearchKeyWordSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    # 北京时间
    try:
        query,_ = await Crud.get_items(db=db, model=searchKeyWord, paging=False, other_filter=[searchKeyWord.id.in_(item.ids)])
        for q in query:

            # 如果不是超级管理员，并且已经锁定，但是不是自己锁定
            if not current_user.is_super and q.is_contact and q.contact_user != current_user.username:
                raise HTTPException(status_code=400, detail='不允许修改其他用户的锁定，谢谢谅解')
            

            q.is_contact = 1
            q.contact_user = current_user.username
            q.last_name = current_user.username
            q.updated_at= get_today(hms=True)

        db.commit()
        
        return Success()
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='修改失败')
    except Exception as e:
        raise HTTPException(status_code=500, detail='请联系超级管理员')


