from fastapi import FastAPI
from api.routers.AdminUser import router as UserRouter
from api.routers.AdminGroup import router as GroupRouter
from api.routers.AdminRole import router as RoleRouter
from api.routers.AdminPermission import router as PermissionRouter
from api.routers.AdminUserLogin import router as UserLoginOrLogout
from api.routers.AdminMemberTag import router as MemberTagRouter
from api.routers.AdminMember import router as MemberRouter
from api.routers.AdminMemberCaiJin import router as MemberCaiJinRouter
from api.routers.AdminMemberCaiJinSource import router as MemberCaiJinSourceRouter
from api.routers.AdminMemberProfile import router as MemberProfileRouter
from api.routers.AdminIphoneNumber import router as IphoneNumberRouter
from api.routers.AdminWebTag import router as WebTagRouter
from api.routers.AdminWebSite import router as WebSiteRouter
from api.routers.AdminKeyWord import router as KeyWordRouter
from api.routers.AdminKeyWordSearch import router as KeyWordSearchRouter
from api.routers.AdminKeyWordSearchCount import router as AdminKeyWordSearchCountRouter
from api.routers.AdminWeight import router as WeightRouter
from api.routers.AdminWeightSearch import router as WeightSearchRouter
from api.routers.AdminWeightSearchCount import router as WeightSearchCount
from api.routers.outMoney.RecordOutMoneyRouter import router as RecordOutMoneyRouter

PREFIX = "/admin"

def init_router(app: FastAPI) -> None:
    app.include_router(UserLoginOrLogout, prefix=PREFIX, tags=['Login'])
    app.include_router(UserRouter,        prefix=PREFIX, tags=['User'])
    app.include_router(GroupRouter,       prefix=PREFIX, tags=['Group'])
    app.include_router(RoleRouter,        prefix=PREFIX, tags=['Role'])
    app.include_router(PermissionRouter,  prefix=PREFIX, tags=['Permission'])


    # 会员汇总
    app.include_router(MemberCaiJinRouter, prefix=PREFIX, tags=['MemberCaiJin'])
    app.include_router(MemberCaiJinSourceRouter, prefix=PREFIX, tags=['MemberCaiJinSource'])
    app.include_router(MemberTagRouter,    prefix=PREFIX, tags=['MemberTag'])
    app.include_router(MemberRouter,       prefix=PREFIX, tags=['Member'])
    app.include_router(MemberProfileRouter,       prefix=PREFIX, tags=['MemberProfile'])
    app.include_router(IphoneNumberRouter,       prefix=PREFIX, tags=['IphoneNumber'])
    
    

    # 站点汇总
    app.include_router(WebTagRouter,      prefix=PREFIX, tags=['WebTag'])
    app.include_router(WebSiteRouter,     prefix=PREFIX, tags=['WebSite'])


    # 关键词
    app.include_router(KeyWordRouter,     prefix=PREFIX, tags=['KeyWord'])
    app.include_router(KeyWordSearchRouter,     prefix=PREFIX, tags=['SearchKeyWord'])
    app.include_router(AdminKeyWordSearchCountRouter,     prefix=PREFIX, tags=['SearchKeyWordCount'])
    


    # 权重域名
    app.include_router(WeightRouter,          prefix=PREFIX, tags=['Weight'])
    app.include_router(WeightSearchRouter,    prefix=PREFIX, tags=['WeightSearch'])
    app.include_router(WeightSearchCount,     prefix=PREFIX, tags=['WeightSearchCount'])



    # 出款管理
    app.include_router(RecordOutMoneyRouter, prefix=PREFIX, tags=['RecordOutMoney'])