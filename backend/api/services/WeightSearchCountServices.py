
from api.models import SearchWeight
from sqlalchemy import and_,func, case
import collections
 
class Services:
    
    # 获取所有类型
    async def get_weight_en(self, db):
        ens = db.query(SearchWeight.en).group_by(SearchWeight.en).having(SearchWeight.en != None).all()
        _ens = list(set(map(lambda x:x.en, ens)))
        return _ens
    

    # 获取所有日期
    async def get_weight_date(self, db):
        _dates_query = db.query(func.date_format(SearchWeight.created_at,'%Y-%m-%d').label('created_at')).group_by('created_at').all()
        _dates = list(set(result[0] for result in _dates_query))
        return _dates

    # 获取指定时间用户
    async def get_weight_current_date(self, db, _d):
        users =  db.query(SearchWeight.first_name).filter(SearchWeight.created_at.like(f"{_d}" + "%")).group_by(SearchWeight.first_name).having(SearchWeight.first_name != None).all()
        _users = list(set(map(lambda x:x.first_name, users)))
        return _users

    # 获取排名序号
    async def get_weight_current_number(self, db):
        level =  db.query(SearchWeight.number).group_by(SearchWeight.number).having(SearchWeight.number != None).all()
        _level = list(set(map(lambda x:x.number, level)))
        return _level

    async def counterKeyWord(self, db, _funcs, _d):
        # 查询执行组合 SQL 语句
        qs = db.query(
            *_funcs,
        ).filter(SearchWeight.created_at.between(_d + ' 00:00:00', _d + ' 23:59:59')).group_by('created_at')

        _results = [dict(zip(result.keys(), result)) for result in qs.all()]
        

        # 计算每个用户对应总共的数据，并添加年月日时间
        counter = collections.Counter()
        for _result in _results:
            counter.update(_result)

        # # 再批量添加到字典内,并添加日期时间
        # _dict.update(dict(counter))
        new_dict = dict(counter)
        return new_dict


    # 获取所有关键词统计
    async def get_weight_count_total(self, db, _ens, _dates):
            results = []
            
            for _d in _dates:
                _funcs = []
                for _e in _ens:
                    _funcs.append(
                            func.sum(case(whens=[(and_(SearchWeight.en == _e), 1)],else_=0)).label(_d + '_' + _e),
                        )

                new_dict = await self.counterKeyWord(db, _funcs, _d)


                # 组合给前端的数据
                test = {}
                test['count_at'] = _d
                test['hasChild'] = True
                test['count_total'] = 0
                for _e in _ens:
                    test['count_' + _e + '_total'] = int(new_dict.get(_d + '_' + _e, 0))
                    test['count_total'] = test['count_total'] + int(new_dict.get(_d + '_' + _e, 0))
                
                results.append(test)


            return results

    # 获取当前之前下所有用户统计
    async def get_weight_count_total_load_childs(self, db, _ens, _users, _d):
        results = []
        _funcs = []
        for _u in _users:
            for _e in _ens:
                _funcs.append(
                        func.sum(case(whens=[(and_(SearchWeight.first_name == _u, SearchWeight.en == _e), 1)],else_=0)).label(_u + '_' + _e),
                    )

        new_dict = await self.counterKeyWord(db, _funcs, _d)

        for _u in _users:
            test = {}
            test['time'] = _d
            test['hasChild'] = False
            test['count_at'] = _u
            test['count_total'] = 0
            for _e in _ens:
                test['count_' + _e + '_total'] = int(new_dict.get(_u + '_' + _e, 0))
                test['count_total'] = test['count_total'] +  int(new_dict.get(_u + '_' + _e, 0))
        
            results.append(test)

        results.sort(key=lambda x: x['count_total'], reverse=True)
        return results


    # 获取某一个用户的统计
    async def get_weight_current_user_count_total(self, db, _ens,  _u,_d):
        results = []
        _funcs = []
        for _e  in _ens:
            _funcs.append(
                func.sum(case(whens=[(and_(SearchWeight.first_name == _u, SearchWeight.en == _e), 1)],else_=0)).label(_u + '_' + _e),
            )


        # 查询执行组合 SQL 语句
        qs = db.query(
            *_funcs,
        ).filter(SearchWeight.created_at.between(_d + ' 00:00:00', _d + ' 23:59:59')).group_by(SearchWeight.first_name)

        _results = [dict(zip(result.keys(), result)) for result in qs.all()]
        

        # 计算每个用户对应总共的数据，并添加年月日时间
        counter = collections.Counter()
        for _result in _results:
            counter.update(_result)

        # # 再批量添加到字典内,并添加日期时间
        # _dict.update(dict(counter))
        new_dict = dict(counter)

            
        
        # { count_number: 1,count_sex: 1, count_other: 2, count_wrong: 3  },
        test = {}
        test['count_total'] = 0

        for _e in _ens:
            v = _u + "_" + _e
            test['count_' + _e]   =  int(new_dict[v])
            test['count_total'] = test['count_total']  + int(new_dict[v])

        results.append(test)


        childCols =  [
                    # { "field": 'count_number', "title": '排名' },
                    { "field": 'count_total',  "title": '总统计' },
                    { "field": 'count_sex',    "title": 'SEX' },
                    { "field": 'count_other',  "title": 'OTHER' },
                    { "field": 'count_wrong',  "title": 'WRONG' },
                ]
        res = {"childData": results, "childCols": childCols}
        return res

services = Services()