from fastapi import APIRouter,Depends,Request
from fastapi.encoders import jsonable_encoder
from api.models import Role,Permission
from api.schemas import CreateRoleSchema,UpdateRoleStatusSchema,RoleBindPermissionSchema,UpdateRoleSchema
from api.dependen import CommonQueryParams, get_db, require_token
from api.services import Crud
from sqlalchemy.orm import Session
from api.utils.response import Success
from api.services import LoginCrud


router = APIRouter()



@router.get("/roles/")
@require_token('getListRole,GET')
async def get_list(request: Request, params: CommonQueryParams = Depends(),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query, total = await Crud.get_items(db=db,model=Role, params=params)
    _list = jsonable_encoder(query)
    _total = total
    data = {
        'list': _list,
        'totalCount': _total
    }
    # data['list'].sort(key=lambda x: x['id'], reverse=True)
    return Success(data=data)


@router.get("/role/{id}")
@require_token('getRole,GET')
async def get_role(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=Role, id=id)
    return Success(data=jsonable_encoder(query))
    

@router.post("/role")
@require_token('createRole,POST')
async def create_role(request: Request, item: CreateRoleSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.create_item(
            db=db, 
            model=Role, 
            name=item.name, 
            description=item.description,
            status=item.status,
            permissions = db.query(Permission).filter(Permission.id.in_(item.permissions)).all() if item.permissions else [],
    )
    return Success(data=jsonable_encoder(query))


@router.delete("/role/{id}")
@require_token('deleteRole,DELETE')
async def del_role(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    role = await Crud.show_item(db=db, model=Role, id=id)
    # 删除该角色的权限和用户
    role.users = []
    role.permissions = []


    await Crud.delele_item(db=db, model=Role, id=id)

    return Success()




@router.put("/role/{id}")
@require_token('modifyRole,PUT')
async def update_role(request: Request, item: UpdateRoleSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=Role,
                description=item.description,
                name=item.name,
                # permissions = db.query(Permission).filter(Permission.id.in_(item.permissions)).all() if item.permissions else [],
            )
    return Success(data=jsonable_encoder(query))



@router.put("/role/{id}/status")
@require_token('updateStatusRole,PUT')
async def update_role_status(request: Request, item: UpdateRoleStatusSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.update_status_item(
                db=db, 
                id=id,
                model=Role,
                status=item.status,
            )
    return Success(data=jsonable_encoder(query))



@router.post("/role/{id}/bind/permission")
@require_token('modifyRole,PUT')
async def bind_permission(request: Request, id: int, item: RoleBindPermissionSchema ,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=Role, id=id)
    query.permissions = db.query(Permission).filter(Permission.id.in_(item.permissions)).all() if item.permissions else []
    db.commit()
    db.refresh(query)
    return Success(data=jsonable_encoder(query))




# @router.put("/user/{id}")
# async def update_user(item: UpdateUserOtherSchema, id: int, db: Session = Depends(get_db)):
#     query = Crud.update_item(
#                 db=db, 
#                 id=id,
#                 model=User,
#                 description=item.description,
#                 avatar=item.avatar,
#                 status=item.status
#             )
#     return Success(data=jsonable_encoder(query, exclude=exclude_pattern))








# @router.get("/role")
# async def get_roles(session: get_session = Depends(), query: CommonQueryParams = Depends()):
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



#     for p in result:
#         m = await CrudService(session).get_many_to_many(
#                                     id=p.id,
#                                     middle=admin_role_permission,
#                                     middle_field='role_id',
#                                     right=Permission,
#                                     right_field='permission_id'
#                                 )
#         p.permissions = m

#     _list = jsonable_encoder(result)
#     return Success(data={'list':_list, 'totalCount': len(_list)})


# @router.get("/role/{id}")
# async def get_role(id: int, session: get_session = Depends()):
#     result = await CrudService(session).show(model=model, id=id)

#     permissions = await CrudService(session).get_many_to_many(
#                                             id=id,
#                                             middle=admin_role_permission,
#                                             middle_field='role_id',
#                                             right=Permission,
#                                             right_field='permission_id'
#                                         )
#     # delattr(result, 'permission')
#     # delattr(result, 'user')
#     setattr(result, 'permissions', permissions)
#     return Success(data=jsonable_encoder(result))


# @router.post("/role")
# async def create_role(item: CreateRoleSchema, session: get_session = Depends()):
#     await CrudService(session).create(model=model, name=item.name, description=item.description,status=item.status)
#     return Success()


# @router.put("/role/{id}")
# async def update_role(id: int, item: CreateRoleSchema,  session: get_session = Depends()):
#     s = CrudService(session)
#     await s.info_by_id(model=model, id=id)
#     await s.update(model=model, id=id, name=item.name, description=item.description,status=item.status)
#     return Success() 


# @router.put("/role/{id}/status")
# async def update_role_status(id: int, item: UpdateRoleStatusSchema,  session: get_session = Depends()):
#     s = CrudService(session)
#     await s.info_by_id(model=model, id=id)
#     await s.update(model=model, id=id, status=item.status)
#     return Success() 

# @router.delete("/role/{id}")
# async def delete_role(id: int, session: get_session = Depends()):
#     await CrudService(session).delete(model=model, id=id)
#     return Success()



# @router.get("/role/{id}/bind/permission")
# async def get_bind_permission(id: int, session: get_session = Depends()):

#     result = await CrudService(session).get_many_to_many(
#                                             id=id,
#                                             middle=admin_role_permission,
#                                             middle_field='role_id',
#                                             right=Permission,
#                                             right_field='permission_id'
#                                         )
#     return Success(data=jsonable_encoder(result))




# @router.post("/role/{id}/bind/permission")
# async def bind_permission(id: int, item: RoleBindPermissionSchema ,session: get_session = Depends()):

#     await CrudService(session).many_to_many(
#         id=id,
#         gid=item.permissions,
#         left=Role,
#         right=Permission,
#         middle=admin_role_permission,
#         bind_left="role_id",
#         bind_right="permission_id"
#     )

#     return Success()