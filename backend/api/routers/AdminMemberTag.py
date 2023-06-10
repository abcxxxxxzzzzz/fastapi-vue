from fastapi import APIRouter,Depends,Request
from fastapi.encoders import jsonable_encoder
from api.models import Tag
from api.schemas import CreateTagSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud
from sqlalchemy.orm import Session 
from api.utils.response import Success
from api.services import LoginCrud

router = APIRouter()



@router.get("/member/tags/list/")
@require_token('getListTag,GET')
async def get_tag_list(request: Request, params: CommonQueryParams = Depends(),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query, total = await Crud.get_items(db=db,model=Tag, params=params)


    _list = jsonable_encoder(query)
    _total = total
    data = {
        'list': _list,
        'totalCount': _total,
    }
    return Success(data=data)


@router.get("/member/tag/{id}/show")
@require_token('getTag,GET')
async def get_tag(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=Tag, id=id)
    return Success(data=jsonable_encoder(query))
    

@router.post("/member/tag/create")
@require_token('createTag,POST')
async def create_tag(request: Request, item: CreateTagSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.create_item(
            db=db, 
            model=Tag, 
            name=item.name, 
            color=item.color,
    )
    return Success(data=jsonable_encoder(query))



@router.delete("/member/tag/{id}/delete")
@require_token('deleteTag,DELETE')
async def del_tag(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    
    query = await Crud.show_item(db=db, model=Tag, id=id)
    # 删除标签关联
    query.members = []


    await Crud.delele_item(db=db, model=Tag, id=id)
    return Success()




@router.put("/member/tag/{id}/update")
@require_token('modifyTag,PUT')
async def update_tag(request: Request, item: CreateTagSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=Tag,
                name=item.name,
                color=item.color,
            )
    return Success(data=jsonable_encoder(query))


