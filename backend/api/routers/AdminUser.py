from fastapi import APIRouter,Depends,HTTPException,Request
from fastapi.encoders import jsonable_encoder
from api.models import User,Group,Role
from api.schemas import CreateUserSchema, UpdateUserPwdSchema,UpdateUserStatusSchema,UpdateUserSchema
from api.dependen import CommonQueryParams,get_db,require_token
from api.utils.passwd import hash_password,verify_password
from api.utils.response import Success
from api.services import Crud
from sqlalchemy.orm import Session
from api.services import LoginCrud



router = APIRouter()


exclude_pattern = ['password']

# code: str = Depends(has_permission('getListUser,GET'))
@router.get("/users/")
@require_token('getListUser,GET')
async def get_list(request: Request, params: CommonQueryParams = Depends(), current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # 用户
    query, total = await Crud.get_items(db=db, model=User, keyword_field='username', params=params)
    for i in query:
        i.role_id = [  r.id for r in i.roles ]
        i.group_id = [  r.id for r in i.groups ]

    _list = jsonable_encoder(query, exclude=exclude_pattern)

    # 角色
    roles, _ = await Crud.get_items(db=db,model=Role)
    roles = jsonable_encoder(roles,include=['id', 'name'])

    # 部门
    groups,_ = await Crud.get_items(db=db, model=Group)
    groups = jsonable_encoder(groups, include=['id', 'name'])

    _total = total
    data = {
        'list': _list,
        'roles': roles,
        'groups': groups,
        'totalCount': _total
    }
    # data['list'].sort(key=lambda x: x['id'], reverse=True)
    return Success(data=data)


@router.get("/user/{id}")
@require_token('getUser,GET')
async def get_user(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=User, id=id)
    return Success(data=jsonable_encoder(query, exclude=exclude_pattern))
    

@router.post("/user")
@require_token('createUser,POST')
async def create_user(request: Request, item: CreateUserSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.create_item(
            db=db, 
            model=User, 
            username=item.username, 
            password=hash_password(item.password),
            description=item.description,
            avatar=item.avatar,
            status=item.status,
            roles = db.query(Role).filter(Role.id.in_(item.role_id)).all() if item.role_id else [],
            groups = db.query(Group).filter(Group.id.in_(item.group_id)).all() if item.group_id else []
        )
    return Success(data=jsonable_encoder(query, exclude=exclude_pattern))


@router.delete("/user/{id}")
@require_token('deleteUser,DELETE')
async def del_user(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    super = await Crud.show_item(db=db, model=User, id=id)
    if super.is_super:
        raise HTTPException(status_code=403, detail='不允许删除超级管理员')

    await Crud.delele_item(db=db, model=User, id=id)
    return Success()


@router.put("/user/{id}")
@require_token('modifyUser,PUT')
async def update_user(request: Request, item: UpdateUserSchema, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    if item.password:
        query = await Crud.update_item(
                    db=db, 
                    id=id,
                    model=User,
                    description=item.description,
                    avatar=item.avatar,
                    password=hash_password(item.password),
                    roles = db.query(Role).filter(Role.id.in_(item.role_id)).all() if item.role_id else [],
                    groups = db.query(Group).filter(Group.id.in_(item.group_id)).all() if item.group_id else []
                )
    else:
        query = await Crud.update_item(
                    db=db, 
                    id=id,
                    model=User,
                    description=item.description,
                    avatar=item.avatar,
                    roles = db.query(Role).filter(Role.id.in_(item.role_id)).all() if item.role_id else [],
                    groups = db.query(Group).filter(Group.id.in_(item.group_id)).all() if item.group_id else []
                )
    return Success(data=jsonable_encoder(query, exclude=exclude_pattern))



@router.put("/user/{id}/status")
@require_token('updateStatusUser,PUT')
async def update_user_status(request: Request, item: UpdateUserStatusSchema, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    super = await Crud.show_item(db=db, model=User, id=id)
    if super.is_super:
        raise HTTPException(status_code=403, detail='不允许修改超级管理员状态')

    query = await Crud.update_status_item(
                db=db, 
                id=id,
                model=User,
                status=item.status,
            )
    return Success(data=jsonable_encoder(query))



@router.post("/user/pwd")
async def update_user_pwd(item: UpdateUserPwdSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    if item.password != item.repassword:
        raise HTTPException(status_code=400, detail='输入密码和确认密码不一致')

    if not verify_password(item.oldpassword, current_user.password):
        raise HTTPException(status_code=400, detail='旧密码错误')

    
    current_user.password = hash_password(item.password)
    db.commit()
    db.refresh(current_user)
    return Success(msg='修改成功')


#     result =  await CrudService(session).lists(
#                                                 model=model, 
#                                                 skip         = query.skip, 
#                                                 limit        = query.limit,
#                                                 q_field      = query.q_field,
#                                                 q_value      = query.q_value,
#                                                 filter_field = query.filter_field, 
#                                                 filter_value = query.filter_value,
#                                                 order_field  = query.order_field,
#                                                 order_value  = query.order_value,
#                                                 time_field   = query.time_field,
#                                                 start_time   = query.start_time,
#                                                 end_time     = query.end_time,
#                                             )
#     _list = jsonable_encoder(result,exclude=exclude_pattern)
#     return Success(data={'list':_list, 'totalCount': len(_list)})


# @router.get("/user/{id}")
# async def get_user(id: int, session: get_session = Depends()):
#     result = await CrudService(session).show(model=model, id=id)
    
#     groups = await CrudService(session).get_many_to_many(
#                                             id=id,
#                                             middle=admin_user_group,
#                                             middle_field='user_id',
#                                             right=Group,
#                                             right_field='group_id'
#                                         )

#     roles = await CrudService(session).get_many_to_many(
#                                             id=id,
#                                             middle=admin_user_role,
#                                             middle_field='user_id',
#                                             right=Role,
#                                             right_field='role_id'
#                                         )
#     # 个人角色和组存储
#     # delattr(result, 'group') # 剔除其他
#     # delattr(result, 'role')  # 剔除其他
#     setattr(result, 'groups', groups)
#     setattr(result, 'roles', roles)
#     return Success(data=jsonable_encoder(result, exclude=exclude_pattern))


# @router.post("/user")
# async def create_user(item: CreateUserSchema, session: get_session = Depends()):
#     req = item.dict(exclude_unset=True)
#     username = req['username']
#     password = hash_password(req['password'])
#     await CrudService(session).create(model=model,username=username, password=password)
#     return Success() # 剔除密码


# @router.put("/user/{id}")
# async def update_user(id: int, item: UpdateUserPwdSchema,  session: get_session = Depends()):
#     s = CrudService(session)
#     res = await s.info_by_id(model=model, id=id)
#     password = verify_password(item.old_password, res.password)
#     if not password:
#         return BadrequestException(msg='旧密码错误')
#     await s.update(model=User, id=id, password=hash_password(item.new_password))
#     return Success() 


# @router.put("/user/{id}/status")
# async def update_user_status(id: int, item: UpdateUserStatusSchema,  session: get_session = Depends()):
#     s = CrudService(session)
#     await s.info_by_id(model=model, id=id)
#     await s.update(model=model, id=id, status=item.status)
#     return Success() 


# @router.delete("/user/{id}")
# async def delete_user(id: int, session: get_session = Depends()):
#     await CrudService(session).delete(model=model, id=id)
#     return Success()



# @router.get("/user/{id}/bind/group")
# async def get_bind_group(id: int, session: get_session = Depends()):

#     result = await CrudService(session).get_many_to_many(
#                                             id=id,
#                                             middle=admin_user_group,
#                                             middle_field='user_id',
#                                             right=Group,
#                                             right_field='group_id'
#                                         )
#     return Success(data=jsonable_encoder(result))



# @router.post("/user/{id}/bind/group")
# async def bind_group(id: int, item: UserBindGroupSchema ,session: get_session = Depends()):

#     await CrudService(session).many_to_many(
#         id=id,
#         gid=item.groups,
#         left=User,
#         right=Group,
#         middle=admin_user_group,
#         bind_left="user_id",
#         bind_right="group_id"
#     )

#     return Success()



# @router.get("/user/{id}/bind/role")
# async def get_bind_role(id: int, session: get_session = Depends()):

#     result = await CrudService(session).get_many_to_many(
#                                             id=id,
#                                             middle=admin_user_role,
#                                             middle_field='user_id',
#                                             right=Role,
#                                             right_field='role_id'
#                                         )
#     return Success(data=jsonable_encoder(result))



# @router.post("/user/{id}/bind/role")
# async def bind_role(id: int, item: UserBindRoleSchema ,session: get_session = Depends()):

#     await CrudService(session).many_to_many(
#         id=id,
#         gid=item.roles,
#         left=User,
#         right=Role,
#         middle=admin_user_role,
#         bind_left="user_id",
#         bind_right="role_id"
#     )

#     return Success()




