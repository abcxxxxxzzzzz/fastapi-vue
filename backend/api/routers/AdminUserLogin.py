from fastapi import APIRouter,Depends, Request, WebSocket
from api.utils.response import Success
from api.services import LoginCrud
from api.schemas import LoginSchema
from api.models import User,Permission,Role,Group,Member,WebSite,Weight,keyWord
from api.utils import getPermissionTree, setToRedis, getFromRedis
from fastapi.encoders import jsonable_encoder
from api.services import Crud
from sqlalchemy.orm import Session
from api.dependen import get_db
from functools import lru_cache

router = APIRouter()

from api.dependen import require_token



@router.post("/login")
async def login(request: Request,data: LoginSchema, db: Session = Depends(get_db)):
    access_token = await LoginCrud.login(request=request, db=db, username=data.username, password=data.password)
    # return {"access_token": username, "token_type": "bearer"}
    return Success(data={'token': access_token})



@router.post("/logout")
async def logout(request: Request, current_user: LoginCrud.verify_token = Depends()):
    # 
    #    '''删除 Redis 中用户的数据'''
    # 
    await LoginCrud.logout(request, current_user.username)
    return Success(msg="退出成功")



@lru_cache
@router.get("/getinfo")
async def get_user(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    query = await Crud.show_item(db=db, model=User, id=current_user.id)
    menus = []
    ruleNames = []

    if query.is_super:
        _list,_ = await Crud.get_items(db=db, model=Permission, paging=False)
        menus = _list
    else:
        for i in query.roles:
            if i.status:
                menus = menus + i.permissions

    for i in menus:
        if not i.menu and i.code and i.method and i.status:
            ruleNames.append(f"{i.code},{i.method}")
                
    
    query.menus = getPermissionTree(jsonable_encoder(set(menus)), includeBtn=False)
    query.ruleNames = ruleNames

    # 最后再更新下 Redis 数据库中的数据
    obj = await getFromRedis(request, current_user.username)
    if obj:
        import json
        o = json.loads(obj)
        o['permissions'] = ruleNames
        await setToRedis(request, current_user.username, json.dumps(o))
    return Success(data=jsonable_encoder(query,exclude=['password']))



@lru_cache
@router.get('/getStatistics')
async def get_getStatistics(current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):

    total1 = db.query(User).count()
    total2 = db.query(Role).count()
    total3 = db.query(Group).count()
    total4 = db.query(Permission).count()



    # query2 = [ i.status for i in query2 if i.status ]
    # query3 = [ i.status for i in query3 if i.status ]
    # query4 = [ i.status for i in query4 if i.status ]

    panels = [{
                "title": "User", 
                "value":  total1, 
                "unit": "USERS", 
                "unitColor": "success", 
                "subTitle": "Total", 
                "subValue": total1, 
                "subUnit": "" 
            },
            {
                "title": "Group", 
                "value": total2, 
                "unit": "GROUPS", 
                "unitColor": "danger", 
                "subTitle": "Total", 
                "subValue": total2, 
                "subUnit": "" 
            },
            {
                "title": "Role", 
                "value": total3, 
                "unit": "ROLES", 
                "unitColor": "info", 
                "subTitle": "Total", 
                "subValue": total3, 
                "subUnit": "" 

            },
            {
                "title": "Permission", 
                "value": total4, 
                "unit": "PERMISSIONS", 
                "unitColor": "warning", 
                "subTitle": "Total", 
                "subValue": total4, 
                "subUnit": "" 
            },

        ] 
    return Success(data={'panels': panels})



# @router.get("/getinfo")
# async def info(current_user: tokenService.verify_token = Depends(), session: get_session = Depends()):

#     id = current_user.id
#     s = CrudService(session)
#     result = await s.show(model=User, id=id)
    
#     groups = await s.get_many_to_many(
#                                             id=id,
#                                             middle=admin_user_group,
#                                             middle_field='user_id',
#                                             right=Group,
#                                             right_field='group_id'
#                                         )

#     roles = await s.get_many_to_many(
#                                             id=id,
#                                             middle=admin_user_role,
#                                             middle_field='user_id',
#                                             right=Role,
#                                             right_field='role_id'
#                                         )

#     menus_orm_list = []
#     for r in roles:
#         m = await s.get_many_to_many(
#                                                 id=r.id,
#                                                 middle=admin_role_permission,
#                                                 middle_field='role_id',
#                                                 right=Permission,
#                                                 right_field='permission_id'
#                                             )

#         menus_orm_list = menus_orm_list + m

#     menus = getPermissionTree(jsonable_encoder(menus_orm_list))

#     # 个人角色和组存储
#     # delattr(result, 'group') # 剔除其他
#     # delattr(result, 'role')  # 剔除其他
#     setattr(result, 'groups', groups)
#     setattr(result, 'roles', roles)
#     setattr(result, 'menus', menus)
#     return Success(data=jsonable_encoder(result, exclude=['password']))
