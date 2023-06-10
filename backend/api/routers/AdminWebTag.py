from fastapi import APIRouter,Depends,Request
from fastapi.encoders import jsonable_encoder
from api.models import WebTag
from api.schemas import CreateWebTagSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud
from sqlalchemy.orm import Session 
from api.utils.response import Success
from api.services import LoginCrud

router = APIRouter()



@router.get("/webtags/")
@require_token('getListWebTag,GET')
async def get_web_tag_list(request: Request, params: CommonQueryParams = Depends(),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query, total = await Crud.get_items(db=db,model=WebTag, params=params)


    _list = jsonable_encoder(query)
    _total = total
    data = {
        'list': _list,
        'totalCount': _total,
    }
    return Success(data=data)


@router.get("/webtag/{id}")
@require_token('getWebTag,GET')
async def get_web_tag(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=WebTag, id=id)
    return Success(data=jsonable_encoder(query))
    

@router.post("/webtag")
@require_token('createWebTag,POST')
async def create_web_tag(request: Request, item: CreateWebTagSchema,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.create_item(
            db=db, 
            model=WebTag, 
            name=item.name, 
            color=item.color,
    )
    return Success(data=jsonable_encoder(query))



@router.delete("/webtag/{id}")
@require_token('deleteWebTag,DELETE')
async def del_web_tag(request: Request, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    

    query = await Crud.show_item(db=db, model=WebTag, id=id)
    # 删除标签关联
    query.websites = []

    await Crud.delele_item(db=db, model=WebTag, id=id)
    return Success()




@router.put("/webtag/{id}")
@require_token('modifyWebTag,PUT')
async def update_web_tag(request: Request, item: CreateWebTagSchema, id: int,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=WebTag,
                name=item.name,
                color=item.color,
            )
    return Success(data=jsonable_encoder(query))


