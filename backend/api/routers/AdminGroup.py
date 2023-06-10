from fastapi import APIRouter,Depends,Request
from fastapi.encoders import jsonable_encoder
from api.models import Group,Permission,admin_role_permission
from api.schemas import CreateGroupSchema,UpdateGroupSchema,UpdateGroupStatusSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud
from sqlalchemy.orm import Session 
from api.utils.response import Success
from api.services import LoginCrud

router = APIRouter()



@router.get("/groups/")
@require_token('getListGroup,GET')
async def get_list(request: Request, params: CommonQueryParams = Depends(),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query, total = await Crud.get_items(db=db,model=Group, params=params)
    _list = jsonable_encoder(query)
    _total = total
    data = {
        'list': _list,
        'totalCount': _total
    }

    # data['list'].sort(key=lambda x: x['id'], reverse=True)
    return Success(data=data)


@router.get("/group/{id}")
@require_token('getGroup,GET')
async def get_group(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=Group, id=id)
    return Success(data=jsonable_encoder(query))
    

@router.post("/group")
@require_token('createGroup,POST')
async def create_group(request: Request, item: CreateGroupSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.create_item(
            db=db, 
            model=Group, 
            name=item.name, 
            status=item.status,
            description=item.description,
    )
    return Success(data=jsonable_encoder(query))



@router.delete("/group/{id}")
@require_token('deleteGroup,DELETE')
async def del_group(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    await Crud.delele_item(db=db, model=Group, id=id)
    return Success()




@router.put("/group/{id}")
@require_token('modifyGroup,PUT')
async def update_group(request: Request, item: UpdateGroupSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=Group,
                description=item.description,
                name=item.name,
            )
    return Success(data=jsonable_encoder(query))





@router.put("/group/{id}/status")
@require_token('updateStatusGroup,PUT')
async def update_group_status(request: Request,item: UpdateGroupStatusSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.update_status_item(
                db=db, 
                id=id,
                model=Group,
                status=item.status,
            )
    return Success(data=jsonable_encoder(query))








# from fastapi import APIRouter,Depends
# from fastapi.encoders import jsonable_encoder
# from api.models import Group
# from api.schemas import CreateGroupSchema,UpdateGroupStatusSchema
# from api.utils import CrudService
# from api.dependencies import get_session, CommonQueryParams
# from api.utils.response import Success
# from api.services.token_service import tokenService

# router = APIRouter()
# # router = APIRouter(dependencies=[Depends(tokenService.verify_token)])

# model = Group



# @router.get("/group")
# async def get_groups(session: get_session = Depends(), query: CommonQueryParams = Depends()):
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
#     return Success(data=jsonable_encoder(result))


# @router.get("/group/{id}")
# async def get_group(id: int, session: get_session = Depends()):
#     result = await CrudService(session).show(model=model, id=id)
#     return Success(data=jsonable_encoder(result))


# @router.post("/group")
# async def create_group(item: CreateGroupSchema, session: get_session = Depends()):
#     await CrudService(session).create(model=model, name=item.name, description=item.description,is_active=item.is_active)
#     return Success()


# @router.put("/group/{id}")
# async def update_group(id: int, item: CreateGroupSchema,  session: get_session = Depends()):
#     s = CrudService(session)
#     await s.info_by_id(model=model, id=id)
#     await s.update(model=model, id=id, name=item.name, description=item.description,is_active=item.is_active)
#     return Success() 


# @router.put("/group/{id}/status")
# async def update_group_status(id: int, item: UpdateGroupStatusSchema,  session: get_session = Depends()):
#     s = CrudService(session)
#     await s.info_by_id(model=model, id=id)
#     await s.update(model=model, id=id, status=item.status)
#     return Success() 


# @router.delete("/group/{id}")
# async def delete_group(id: int, session: get_session = Depends()):
#     await CrudService(session).delete(model=model, id=id)
#     return Success()
