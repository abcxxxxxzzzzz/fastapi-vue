from fastapi import APIRouter,Depends,Request,Query,HTTPException
from fastapi.encoders import jsonable_encoder
from api.models import WebSite,WebTag
from api.schemas import CreateWebSiteSchema,multideleteWebSiteSchema,multiSearchWebSiteSchema,importWebSiteDataSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud,LoginCrud,WebSiteServices
from sqlalchemy.orm import Session 
from api.utils.response import Success
from typing import Optional
from sqlalchemy import or_,and_

router = APIRouter()


# @router.post("/member/search/multi")
# @require_token('multiSearchMember,POST')
# async def multi_get_member(request: Request, item: multiSearchMemberSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
#     '''------------------------------------------------'''
#     filters = []
#     batchType = item.batchType
#     batchContent = item.batchContent

#     if len(batchContent) == 0:
#         raise HTTPException(status_code=400, detail='请传入需要查询的内容')

#     elif batchType == 'bank' and current_user.is_super: # 如果是超级管理员，并且搜索的是银行卡信息
#         filters.append(Member.bank.in_(batchContent))

#     elif batchType == 'iphone' and current_user.is_super: # 如果是超级管理员，并且搜索的是手机号码信息
#         filters.append(Member.iphone.in_(batchContent))

#     elif batchType == 'id_number' and current_user.is_super: # 如果是超级管理员，并且搜索的是手机号码信息
#         filters.append(Member.id_number.in_(batchContent))

#     elif batchType == 'username': # 如果搜索的是账户
#         filters.append(Member.username.in_(batchContent))

#     elif batchType == 'realname': # 如果搜索的是会员姓名
#         filters.append(Member.realname.in_(batchContent))
    

#     else:
#         raise HTTPException(status_code=400, detail='请传入规定可以搜索的字段')



#     if item.includeDelete != 2: # 2 代表全部
#         filters.append(Member.is_del==item.includeDelete)


#     if item.owner_id:
#         filters.append(Member.owner_id==item.owner_id)
#     '''------------------------------------------------'''

#     data, _ = await Crud.get_items(db=db, model=Member, paging=False, other_filter=filters)

#     return Success(data=jsonable_encoder(data))













@router.get("/websites/")
@require_token('getListWebSite,GET')
async def get_website_list(request: Request, 
    params: CommonQueryParams = Depends(), 
    tab: Optional[str] = Query(None),
    keywordType: Optional[str] = Query(None), 
    owner_id: Optional[int] = Query(None),
    owner_tag_id: Optional[str] = Query(None), 
    field: Optional[str] = Query(None),
    order_by: Optional[str] = Query(None),
    current_user: LoginCrud.verify_token = Depends(), 
    db: Session = Depends(get_db)
):

    # 设置搜索部门
    if owner_id is not None:
        setattr(params, 'owner_id', owner_id) 

    if keywordType is not None:
        setattr(params, 'keywordType', keywordType)
        
    # 标签搜索
    if owner_tag_id and bool(owner_tag_id):
        _tags = list(map(int, owner_tag_id.split(','))) or list[int(owner_tag_id)]
        setattr(params, '_tags', _tags) 
        # filters.append(Member.tag)
        # filters.append(Tag.id.in_(_tags))
    # tab 标签切换，搜索是否删除字段
    setattr(params, 'is_del', 0) if tab == 'all' else setattr(params, 'is_del', 1)
    

    # 获取排序
    # if field and order_by:
        # await WebSiteServices.get_order_field(
        #     model=WebSite,
        #     field=field,
        #     order_by=order_by,
        # )

    data = await WebSiteServices.get_list(current_user=current_user, db=db, model=WebSite, params=params, tab=tab, field=field, order_by=order_by)


    # data = await WebSiteServices.get_list(current_user=current_user, db=db, model=WebSite, params=params, tab=tab)


   
    return Success(data=data)


# @router.get("/member/{id}")
# @require_token('getMember,GET')
# async def get_member(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
#     query = await Crud.show_item(db=db, model=Member, id=id)
#     return Success(data=jsonable_encoder(query))
    

@router.post("/website")
@require_token('createWebSite,POST')
async def create_website(request: Request, item: CreateWebSiteSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    '''------------------------------------------------'''
    # 如果不是超级用户
    if not current_user.is_super:
        # 获取当前用户所属组
        userGroups = [ g.id for g in current_user.groups]
        
        # 判断如果数据不是用户所属组，不允许修改
        if item.owner_id not in userGroups:
            raise HTTPException(status_code=403, detail='不允许创建其他部门数据')
    '''------------------------------------------------'''
    
    filters = []
    filters.append(and_(
        WebSite.channel_code==item.channel_code,
        WebSite.is_del==0
    ))
    filters.append(WebSite.owner_id==item.owner_id)

    is_exits,_ = await Crud.get_items(db=db, model=WebSite,other_filter=filters)

    if is_exits:
        raise HTTPException(status_code=403, detail=f'归属系列：{is_exits[0].owner.name}， 已存在渠道号: {item.channel_code}')

    query = await Crud.create_item(
            db=db, 
            model=WebSite, 
            name=item.name, 
            child=','.join(item.child),
            channel_code=item.channel_code,
            contact=item.contact,
            parent_id=item.parent_id  or 0,
            wallet_address=item.wallet_address,
            description=item.description,
            first_name=current_user.username,
            tags = db.query(WebTag).filter(WebTag.id.in_(item.tag_id)).all() if item.tag_id else [],
            owner_id=item.owner_id,
            gg_position = item.gg_position,
            gg_price = item.gg_price,
            gg_time = item.gg_time,
            gg_effect = item.gg_effect,
            op_link = item.op_link,

    )

    return Success(data=jsonable_encoder(query))



# 删除
@router.delete("/website/{id}")
@require_token('deleteWebSite,DELETE')
async def del_website(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    # 如果不是超级用户
    if not current_user.is_super:
        # 获取当前用户所属组
        userGroups = [ g.id for g in current_user.groups]
        
        # 获取需要修改数据的归属部门
        obj = await Crud.show_item(db, WebSite, id)
        
        # 判断如果数据不是用户所属组，不允许修改
        if obj.owner_id not in userGroups:
            raise HTTPException(status_code=403, detail='不允许删除其他部门数据')
    '''------------------------------------------------'''

    await Crud.delele_item(db=db, model=WebSite, id=id, recover=True, last_name=current_user.username)
    return Success()



# 改
@router.put("/website/{id}")
@require_token('modifyWebSite,PUT')
async def update_website(request: Request, item: CreateWebSiteSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    '''------------------------------------------------'''
    # 如果不是超级用户
    if not current_user.is_super:
        # 获取当前用户所属组
        userGroups = [ g.id for g in current_user.groups]
        
        # 获取需要修改数据的归属部门
        obj = await Crud.show_item(db, WebSite, id)
        
        # 判断如果数据不是用户所属组，不允许修改
        if obj.owner_id not in userGroups:
            raise HTTPException(status_code=403, detail='不允许修改其他部门数据')
    '''------------------------------------------------'''

    filters = []
    filters.append(and_(
        WebSite.channel_code==item.channel_code,
        WebSite.is_del == 0,
    ))
    filters.append(WebSite.owner_id==item.owner_id)
    filters.append(WebSite.id != id)

    is_exits,_ = await Crud.get_items(db=db, model=WebSite,other_filter=filters)

    if is_exits:
        raise HTTPException(status_code=403, detail=f'归属系列：{is_exits[0].owner.name}， 已存在渠道号: {item.channel_code}')


    query = await Crud.update_item(
                db=db, 
                id=id,
                model=WebSite,
                name=item.name, 
                child=','.join(item.child),
                channel_code=item.channel_code,
                contact=item.contact,
                parent_id=item.parent_id  or 0,
                wallet_address=item.wallet_address,
                description=item.description,
                # first_name=current_user.username,
                last_name=current_user.username,
                tags = db.query(WebTag).filter(WebTag.id.in_(item.tag_id)).all() if item.tag_id else [],
                owner_id=item.owner_id,
                gg_position = item.gg_position,
                gg_price = item.gg_price,
                gg_time = item.gg_time,
                gg_effect = item.gg_effect,
                op_link = item.op_link,
            )
    return Success(data=jsonable_encoder(query))




'''批量删除'''
@router.post("/website/multi")
@require_token('multideleteWebSite,POST')
async def multi_del_website(request: Request, item: multideleteWebSiteSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    # 如果不是超级用户
    if not current_user.is_super:
        # 获取当前用户所属组
        userGroups = [ g.id for g in current_user.groups]

        # 获取需要删除的 ids 对应的组
        ids_obj,_ = await Crud.get_items(model=WebSite, db=db, other_filter=[WebSite.id.in_(item.ids)])
        ids_groups = list(set(map(lambda x:x.owner_id, ids_obj)))

        # 通过差集的方式获取不同，判断如果数据不是用户所属组，不允许批量删除
        if list(set(ids_groups).difference(set(userGroups))):
            raise HTTPException(status_code=403, detail='不允许删除其他部门数据')
    '''------------------------------------------------'''

    await Crud.multi_delete(db=db, model=WebSite, ids=item.ids, last_name=current_user.username)
    return Success()




'''批量回收还原'''
@router.post("/website/recover")
@require_token('multirecoverWebSite,POST')
async def multi_rec_website(request: Request, item: multideleteWebSiteSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    # 如果不是超级用户
    if not current_user.is_super:
        # 获取当前用户所属组
        userGroups = [ g.id for g in current_user.groups]
        
        # 获取需要删除的 ids 对应的组
        ids_obj,_ = await Crud.get_items(model=WebSite, db=db, other_filter=[WebSite.id.in_(item.ids)])
        ids_groups = list(set(map(lambda x:x.owner_id, ids_obj)))

        # 通过差集的方式获取不同，判断如果数据不是用户所属组，不允许批量删除
        if list(set(ids_groups).difference(set(userGroups))):
            raise HTTPException(status_code=403, detail='不允许还原其他部门数据')
        
    '''------------------------------------------------'''

    await Crud.recover_delete(db=db, model=WebSite, ids=item.ids, last_name=current_user.username)
    return Success()


'''批量彻底删除'''
@router.post("/website/clear")
@require_token('multiclearWebSite,POST')
async def multi_clear_website(request: Request, item: multideleteWebSiteSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    # 如果不是超级用户
    if not current_user.is_super:
        # 获取当前用户所属组
        userGroups = [ g.id for g in current_user.groups]
        
        # 获取需要删除的 ids 对应的组
        ids_obj,_ = await Crud.get_items(model=WebSite, db=db, other_filter=[WebSite.id.in_(item.ids)])
        ids_groups = list(set(map(lambda x:x.owner_id, ids_obj)))

        # 通过差集的方式获取不同，判断如果数据不是用户所属组，不允许批量删除
        if list(set(ids_groups).difference(set(userGroups))):
            raise HTTPException(status_code=403, detail='不允许清空其他部门数据')
        
    '''------------------------------------------------'''

    await Crud.clear_delete(db=db, model=WebSite, ids=item.ids)
    return Success()




'''批量搜索'''
@router.post("/website/search/multi")
@require_token('multiSearchWebSite,POST')
async def multi_get_member(request: Request, item: multiSearchWebSiteSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    '''------------------------------------------------'''
    filters = []
    batchType = item.batchType
    batchContent = item.batchContent

    if len(batchContent) == 0:
        raise HTTPException(status_code=400, detail='请传入需要查询的内容')

    elif batchType == 'name': # 搜索主域和子域
        filters.append(or_(
                WebSite.name.in_(batchContent),
                WebSite.child.in_(batchContent),
            ))

    elif batchType == 'channel_code': # 搜索渠道编号
        filters.append(WebSite.channel_code.in_(batchContent))


    elif batchType == 'contact': # 搜索联系方式
        filters.append(WebSite.contact.in_(batchContent))



    elif batchType == 'wallet_address': # 搜索钱包地址
        filters.append(WebSite.wallet_address.in_(batchContent))

    

    else:
        raise HTTPException(status_code=400, detail='请传入规定可以搜索的字段')



    if item.includeDelete != 2: # 2 代表全部
        filters.append(WebSite.is_del==item.includeDelete)


    if item.owner_id:
        filters.append(WebSite.owner_id==item.owner_id)
    '''------------------------------------------------'''

    data, _ = await Crud.get_items(db=db, model=WebSite, paging=False, other_filter=filters)

    return Success(data=jsonable_encoder(data))






'''批量导入'''
@router.post("/website/import")
@require_token('importExcelWebSite,POST')
async def multi_get_member(request: Request, item: importWebSiteDataSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    await WebSiteServices.import_excel(db=db, current_user=current_user, params=item)
    return Success()



'''批量更新'''
@router.post("/website/modify/multi")
@require_token('multiModifyWebSite,POST')
async def multi_modify_member(request: Request, item: multiSearchWebSiteSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
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
            

    
    await WebSiteServices.batch_modify(db=db, params=item, current_user=current_user)

    return Success()