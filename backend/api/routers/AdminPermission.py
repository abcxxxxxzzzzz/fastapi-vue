from fastapi import APIRouter,Depends,Request
from fastapi.encoders import jsonable_encoder
from api.models import Permission
from api.schemas import CreatePermissionSchema,UpdatePermissionStatusSchema,UpdatePermissionSchema
from api.dependen import get_db,require_token
from api.services import Crud
from sqlalchemy.orm import Session
from api.utils.response import Success
from api.utils import getPermissionTree
from api.services import LoginCrud

router = APIRouter()



@router.get("/permissions")
# async def get_list(params: CommonQueryParams = Depends(), db: Session = Depends(get_db)):
@require_token('getListPermission,GET')
async def get_list(request: Request, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query, total = await Crud.get_items(db=db,model=Permission, paging=False)
    _list = jsonable_encoder(query)


    _total = total
    data = {
        'list': getPermissionTree(jsonable_encoder(_list)),
        'totalCount': _total
    }

    # data['list'].sort(key=lambda x: x['id'], reverse=True)
    return Success(data=data)


@router.get("/permission/{id}")
@require_token('getPermission,GET')
async def get_permission(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=Permission, id=id)
    return Success(data=jsonable_encoder(query))
    

@router.post("/permission")
@require_token('createPermission,POST')
async def create_permission(request: Request, item: CreatePermissionSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.create_item(
            db=db, 
            model=Permission, 
            name=item.name, 
            menu=item.menu, 
            code=item.code, 
            frontpath=item.frontpath, 
            method=item.method, 
            icon=item.icon, 
            sort=item.sort, 
            parent_id=item.parent_id, 
            status=item.status, 
            
    )
    return Success(data=jsonable_encoder(query))


@router.delete("/permission/{id}")
@require_token('deletePermission,DELETE')
async def del_permission(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    # 剔除关联权限
    _a = await Crud.show_item(db=db, model=Permission, id=id)
    _a.roles = []
    
    # 再次删除
    await Crud.delele_item(db=db, model=Permission, id=id)
    return Success()




@router.put("/permission/{id}")
@require_token('modifyPermission,PUT')
async def update_permission(request: Request, item: UpdatePermissionSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=Permission,
                name=item.name,
                menu=item.menu, 
                code=item.code, 
                frontpath=item.frontpath, 
                method=item.method, 
                icon=item.icon, 
                sort=item.sort, 
                parent_id=item.parent_id, 
            )
    return Success(data=jsonable_encoder(query))



@router.put("/permission/{id}/status")
@require_token('updateStatusPermission,PUT')
async def update_permission_status(request: Request, item: UpdatePermissionStatusSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.update_status_item(
                db=db, 
                id=id,
                model=Permission,
                status=item.status,
            )
    return Success(data=jsonable_encoder(query))
















# from fastapi import APIRouter,Depends
# from fastapi.encoders import jsonable_encoder
# from api.models import Permission
# from api.schemas import CreatePermissionSchema,UpdatePermissionStatusSchema,PermissionOutSchema
# from api.utils import CrudService,getPermissionTree
# from api.dependencies import get_session, CommonQueryParams
# from api.utils.response import Success
# from api.services.token_service import tokenService

# router = APIRouter()
# # router = APIRouter(dependencies=[Depends(tokenService.verify_token)])

# model = Permission


# @router.get("/permission")
# async def get_permissions(session: get_session = Depends(), query: CommonQueryParams = Depends()):
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
#     tree = getPermissionTree(jsonable_encoder(result))
#     return Success(data={'list':tree, 'totalCount': len(tree)})


# @router.get("/permission/{id}")
# async def get_permission(id: int, session: get_session = Depends()):
#     result = await CrudService(session).show(model=model, id=id)
#     return Success(data=jsonable_encoder(result))


# @router.post("/permission")
# async def create_permission(item: CreatePermissionSchema, session: get_session = Depends()):
#     await CrudService(session).create(
#             model=model, 
#             name=item.name,
#             menu=item.menu, 
#             code=item.code,
#             frontpath=item.frontpath,
#             method=item.method,
#             icon=item.icon,
#             sort=item.sort,
#             status=item.status,
#             parent_id=item.parent_id,
#         )
#     return Success()


# @router.put("/permission/{id}")
# async def update_permission(id: int, item: CreatePermissionSchema,  session: get_session = Depends()):
#     s = CrudService(session)
#     await s.info_by_id(model=model, id=id)
#     await s.update(
#             id=id,
#             model=model, 
#             name=item.name,
#             menu=item.menu, 
#             code=item.code,
#             frontpath=item.frontpath,
#             method=item.method,
#             icon=item.icon,
#             sort=item.sort,
#             status=item.status,
#             parent_id=item.parent_id,
#         )
#     return Success() 


# @router.put("/permission/{id}/status")
# async def update_permission_status(id: int, item: UpdatePermissionStatusSchema,  session: get_session = Depends()):
#     s = CrudService(session)
#     await s.info_by_id(model=model, id=id)
#     await s.update(model=model, id=id, status=item.status)
#     return Success() 



# @router.delete("/permission/{id}")
# async def delete_permission(id: int, session: get_session = Depends()):
#     await CrudService(session).delete(model=model, id=id)
#     return Success()
