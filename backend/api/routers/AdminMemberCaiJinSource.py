from fastapi import APIRouter,Depends,Request,Query
from fastapi.encoders import jsonable_encoder
from api.models import MemberCaiJinSource
from api.schemas import CreateMemberCaiJinSourceSchema
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import Crud
from sqlalchemy.orm import Session 
from api.utils.response import Success
from api.services import LoginCrud
from typing import Optional

router = APIRouter()



@router.get("/member/caijin/source/list/")
@require_token('getMemberCaiJinSourceList,GET')
async def get_member_caijin_source_list(request: Request, paging: Optional[int] = Query(1), params: CommonQueryParams = Depends(), current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    query, total = await Crud.get_items(db=db,model=MemberCaiJinSource, paging=bool(paging), params=params)


    _list = jsonable_encoder(query)
    _total = total
    data = {
        'list': _list,
        'totalCount': _total,
    }
    return Success(data=data)


@router.get("/member/caijin/source/{id}/show")
@require_token('getMemberCaiJinSourceShow,GET')
async def get_member_caijin_source(request: Request, id: int, db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=MemberCaiJinSource, id=id)
    return Success(data=jsonable_encoder(query))
    

@router.post("/member/caijin/source/create")
@require_token('getMemberCaiJinSourceCreate,POST')
async def create_member_caijin_source(request: Request, item: CreateMemberCaiJinSourceSchema, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.create_item(
            db=db, 
            model=MemberCaiJinSource, 
            name=item.name, 
            color=item.color,
    )
    return Success(data=jsonable_encoder(query))



@router.delete("/member/caijin/source/{id}/delete")
@require_token('getMemberCaiJinSourceDelete,DELETE')
async def del_member_caijin_source(request: Request, id: int, current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    

    query = await Crud.show_item(db=db, model=MemberCaiJinSource, id=id)
    # 删除标签关联
    query.websites = []

    await Crud.delele_item(db=db, model=MemberCaiJinSource, id=id)
    return Success()




@router.put("/member/caijin/source/{id}/update")
@require_token('getMemberCaiJinSourceUpdate,PUT')
async def update_member_caijin_source(request: Request, item: CreateMemberCaiJinSourceSchema, id: int,current_user: LoginCrud.verify_token = Depends(),  db: Session = Depends(get_db)):
    query = await Crud.update_item(
                db=db, 
                id=id,
                model=MemberCaiJinSource,
                name=item.name,
                color=item.color,
            )
    return Success(data=jsonable_encoder(query))


