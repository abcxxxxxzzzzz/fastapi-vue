from fastapi import APIRouter,Depends,Request,HTTPException,Query
from sqlalchemy.orm import Session
from typing import Optional
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import WeightSearchCountServices
from api.utils.response import Success
from api.services import LoginCrud



router = APIRouter()



@router.get("/count/searchweights/total/")
@require_token('getSearchWeightCount,GET')
async def get_searchweight_cout_total(request: Request, tday: Optional[str] = Query(None), params: CommonQueryParams = Depends(), current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
        # 获取所有类型
        _ens = await WeightSearchCountServices.get_weight_en(db)

        # 获取所有日期
        _dates_query = await WeightSearchCountServices.get_weight_date(db)
        _dates = sorted(_dates_query, reverse=True)

        if tday:
            _results = await WeightSearchCountServices.get_weight_count_total(db, _ens, tday.split(','))
        else:
            _results = await WeightSearchCountServices.get_weight_count_total(db, _ens, _dates[params.skip-1:params.limit])

        results = {
            'list': _results,
            'history':_dates,
            'total': len(_dates)
        }

        return Success(data=results)





@router.get("/count/searchweights/load/childs/")
@require_token('getSearchWeightCount,GET')
async def get_searchword_load_childs(request: Request, sday: Optional[str] = Query(None),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    if not sday:
        raise HTTPException(status_code=400, detail='参数错误, 请传入查询日期,日期格式： 1970-01-12')

    # 获取所有类型
    _ens = await WeightSearchCountServices.get_weight_en(db)

    # 获取指定查询时间的用户
    _users = await WeightSearchCountServices.get_weight_current_date(db=db, _d=sday)

    results = await WeightSearchCountServices.get_weight_count_total_load_childs(db=db, _ens=_ens, _users=_users, _d=sday)
    return Success(data=results)



@router.get("/count/searchweights/expand/childs/")
@require_token('getSearchWeightCount,GET')
async def get_searchword_expand_childs(request: Request, ssday: Optional[str] = Query(None), user: Optional[str] = Query(None), current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    if not user and not ssday:
        raise HTTPException(status_code=400, detail='参数错误, 请传入查询日期和用户')

    _u = user
    _d = ssday

    # 获取所有类型
    _ens = await WeightSearchCountServices.get_weight_en(db)

    # 获取指定时间的所有排名
    results = await WeightSearchCountServices.get_weight_current_user_count_total(db, _ens, _u, _d)
    return Success(data=results)