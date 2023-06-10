
from fastapi import APIRouter,Depends,Request,HTTPException,Query
from api.dependen import CommonQueryParams,get_db, require_token
from api.services import SearchKeyWordCountServices
from sqlalchemy.orm import Session
from api.utils.response import Success
from api.services import LoginCrud
from typing import Optional



router = APIRouter()


# # 获取已统计的时间
# @lru_cache
# @router.get("/count/searchkeywords/groupby/time")
# @require_token('getSearchKeyWordCount,GET')
# async def get_searchkeyword_group_by_count_at(request: Request,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
#     _group_by_count_at = await Crud.group_by(db=db, model=countSearchKeyWord.count_at, _group_by=countSearchKeyWord.count_at)
#     group_by_count_at = sorted(_group_by_count_at, reverse=True)
#     return Success(data={'count_ats': jsonable_encoder(group_by_count_at)})


# # 计算当前时间的历史数据
# @lru_cache
# @router.get('/batch/count/searchkeywords')
# @require_token('getSearchKeyWordCount,GET')
# async def batch_count_keyword(request: Request, background_tasks: BackgroundTasks, current_user: LoginCrud.verify_token = Depends(),  db: Session = Depends(get_db)):
    
#     background_tasks.add_task(SearchKewWordServices.batch_count_history, db)

#     # data = SearchKewWordServices.batch_count_history(db)
#     # return Success(data=data)
#     return Success(data=[], msg='历史查询任务已提交，请稍后刷新查看')



# @lru_cache
# @router.get("/count/searchkeywords")
# @require_token('getSearchKeyWordCount,GET')
# async def get_searchkeyword_group_by(request: Request, today: Union[str, None] = None,current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):



#     _list = await SearchKewWordServices.get_count_today(db)
#     total = len(_list)
    


#     # _list, total = await Crud.get_items(db=db, model=countSearchKeyWord, paging=False)
    
    
#     _list.sort(key=lambda x: x['count_number'], reverse=False)

#     data = {
#         'list': _list,
#         'totalCount': total,
#     }
#     return Success(data=data)







@router.get("/count/searchkeywords/total/")
@require_token('getSearchKeyWordCount,GET')
async def get_searchkeyword_cout_total(request: Request, tday: Optional[str] = Query(None), params: CommonQueryParams = Depends(), current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
        # 获取所有类型
        _ens = await SearchKeyWordCountServices.get_keyword_en(db)

        # 获取所有日期
        _dates_query = await SearchKeyWordCountServices.get_keyword_date(db)
        _dates = sorted(_dates_query, reverse=True)

        if tday:
            _results = await SearchKeyWordCountServices.get_keyword_count_total(db, _ens, tday.split(','))
        else:
            _results = await SearchKeyWordCountServices.get_keyword_count_total(db, _ens, _dates[params.skip-1:params.limit])

        results = {
            'list': _results,
            'history':_dates,
            'total': len(_dates)
        }

        return Success(data=results)





@router.get("/count/searchkeywords/load/childs/")
async def get_searchword_load_childs(request: Request, sday: Optional[str] = Query(None),current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    if not sday:
        raise HTTPException(status_code=400, detail='参数错误, 请传入查询日期,日期格式： 1970-01-12')

    # 获取所有类型
    _ens = await SearchKeyWordCountServices.get_keyword_en(db)

    # 获取指定查询时间的用户
    _users = await SearchKeyWordCountServices.get_keyword_current_date(db=db, _d=sday)

    results = await SearchKeyWordCountServices.get_keyword_count_total_load_childs(db=db, _ens=_ens, _users=_users, _d=sday)
    return Success(data=results)



@router.get("/count/searchkeywords/expand/childs/")
async def get_searchword_expand_childs(request: Request, ssday: Optional[str] = Query(None), user: Optional[str] = Query(None), current_user: LoginCrud.verify_token = Depends(), db: Session = Depends(get_db)):
    
    if not user and not ssday:
        raise HTTPException(status_code=400, detail='参数错误, 请传入查询日期和用户')

    _u = user
    _d = ssday

    # 获取所有类型
    _ens = await SearchKeyWordCountServices.get_keyword_en(db)

    # 获取指定时间的所有排名
    _level = await SearchKeyWordCountServices.get_keyword_current_number(db)
    results = await SearchKeyWordCountServices.get_keyword_current_user_count_total(db, _ens,_level, _u, _d)
    return Success(data=results)