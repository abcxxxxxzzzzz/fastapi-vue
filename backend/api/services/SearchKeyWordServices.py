from api.models import searchKeyWord,countSearchKeyWord
from sqlalchemy import and_,func, case
import collections
from api.utils import get_today


class Services:

    def get_keyword_user(self, db):
        users =  db.query(searchKeyWord.first_name).group_by(searchKeyWord.first_name).having(searchKeyWord.first_name != None).all()
        _users = list(set(map(lambda x:x.first_name, users)))
        return _users

    def get_keyword_number(self, db):
        level =  db.query(searchKeyWord.number).group_by(searchKeyWord.number).having(searchKeyWord.number != None).all()
        _level = list(set(map(lambda x:x.number, level)))
        return _level


    def get_keyword_en(self, db):
        ens = db.query(searchKeyWord.en).group_by(searchKeyWord.en).having(searchKeyWord.en != None).all()
        _ens = list(set(map(lambda x:x.en, ens)))
        return _ens
    

    def get_keyword_date(self, db):
        _dates_query = db.query(func.date_format(searchKeyWord.created_at,'%Y-%m-%d').label('created_at')).group_by('created_at').all()
        _dates = list(set(result[0] for result in _dates_query))
        return _dates



    def get_today(self):
        _now = get_today()
        return _now


    def is_exists_db(self, db, data):
        d1 = db.query(countSearchKeyWord).filter(countSearchKeyWord.count_at.in_(data)).all()
        d2 = list(set(map(lambda x:x.count_at, d1)))

        new_data = list(set(data).difference(set(d2)))

        return new_data




    def modify_data(self, _k, data):
        _data = []
        for _d in data:
            for k, v in _d.items():
                for _u in v[_k]:
                    _data.append(_u)
        return _data


        

    def modify_to_db(self, data):
        if not data:
            return False

        _data = []
        # 组合唯一数据
        for d in data:
            _d = {}
            _d['count_number'] = d['level']
            _d['count_user'] = d['username']
            _d['count_at'] = d['created_at']
            _d['count_total'] = 0
            _d['count_sex'] = 0
            _d['count_other'] = 0
            _d['count_wrong'] = 0

            if _d not in _data:
                _data.append(_d)

        # 获取类型对应数值
        for _d in _data:
            for d in data:
                if _d['count_number'] == d['level'] and _d['count_user'] == d['username'] and _d['count_at'] == d['created_at']:
                    if d['type'] == 'sex':
                        _d['count_sex'] = d['count']

                    if d['type'] == 'other':
                        _d['count_other'] = d['count']

                    if d['type'] == 'wrong':
                        _d['count_wrong'] = d['count']

                    _d['count_total'] = _d['count_total'] + d['count'] 
                    

        return _data

        

    def insert_to_db(self,db, data):
        db.execute(
            countSearchKeyWord.__table__.insert(data)
        )
        db.commit()

        
    
    def batch_count_history(self, db, message=''): 

        # 获取关键词汇总用户
        _users =   self.get_keyword_user(db)

        # 获取关键词汇总排名序号
        _level =  self.get_keyword_number(db)

        # 获取关键词汇总所有类型
        _ens   = self.get_keyword_en(db)

        
        # # 获取关键词汇总所有年月日, 剔除今天日期
        _today = self.get_today()
        _dates = self.get_keyword_date(db=db)
        _dates.remove(_today)


        _dates = self.is_exists_db(db=db, data=_dates)
        # 如果数据库已经存在历史数据，则不执行
        if _dates:
            # 计算历史所有年月日数据, 剔除今天
            res = []
            for _d in _dates:
                results = []
                _funcs = []

                # 关键词汇总所有用户，所有排名级别数据组合 SQL 语句
                for _u in _users:
                    for _l in _level:
                        for _e  in _ens:
                            _funcs.append(
                                func.sum(case(whens=[(and_(searchKeyWord.first_name == _u, searchKeyWord.number == _l, searchKeyWord.en == _e), 1)],else_=0)).label(_u + '_' + str(_l) + '_' + _e),
                            )

                _dict = {}

                # 查询执行组合 SQL 语句
                qs = db.query(
                    func.count().label("total"),
                    *_funcs,
                ).filter(searchKeyWord.created_at.between(_d + ' 00:00:00', _d + ' 23:59:59')).group_by('created_at')

                _results = [dict(zip(result.keys(), result)) for result in qs.all()]
                

                # 计算每个用户对应总共的数据，并添加年月日时间
                counter = collections.Counter()
                for _result in _results:
                    counter.update(_result)

                # # 再批量添加到字典内,并添加日期时间
                _dict.update(dict(counter))
                
                _dict['created_at'] = _d
                results.append(_dict)


                # 组合成我们想要的数据
                _k1 = 'created_at'
                _k2 = 'users'
                _k3 = 'total'
                _k4 = 'username'
                _k5 = 'level'
                _k6 = 'count'
                _k7 = 'type'

                
                
                for _u in _users:
                    for _d in results:
                        _res = {}
                        _res.update({_d[_k1]: {_k2: [], _k3: 0}})
                        for _l in _level:
                            for _e in _ens:
                                _res[_d[_k1]][_k2].append({_k4: _u, _k5: _l, _k6: int(_d[_u + '_' + str(_l) + '_' + _e]), _k1: _d[_k1], _k7: _e})

                        _res[_d[_k1]][_k3] = _d[_k3]
                        res.append(_res) 

            resNew = self.modify_data(_k2,res)
            db_data = self.modify_to_db(resNew)
            
            # with open("log.txt", mode="w") as log:
            #     log.write(str(db_data))


            self.insert_to_db(db, db_data)





    async def asy_get_keyword_user(self, db, _today):
        users =  db.query(searchKeyWord.first_name).filter(searchKeyWord.created_at.like(f"{_today}" + "%")).group_by(searchKeyWord.first_name).having(searchKeyWord.first_name != None).all()
        _users = list(set(map(lambda x:x.first_name, users)))
        return _users

    async def asy_get_keyword_number(self, db, _today):
        level =  db.query(searchKeyWord.number).filter(searchKeyWord.created_at.like(f"{_today}" + "%")).group_by(searchKeyWord.number).having(searchKeyWord.number != None).all()
        _level = list(set(map(lambda x:x.number, level)))
        return _level


    async def asy_get_keyword_en(self, db, _today):
        ens = db.query(searchKeyWord.en).filter(searchKeyWord.created_at.like(f"{_today}" + "%")).group_by(searchKeyWord.en).having(searchKeyWord.en != None).all()
        _ens = list(set(map(lambda x:x.en, ens)))
        return _ens

    async def asy_get_today(self):
        _now = get_today()
        return _now


    async def asy_get_res(self, db, _d, _users, _level, _ens):
        res = []
        results = []
        _funcs = []
        _dict = {}

        # 关键词汇总所有用户，所有排名级别数据组合 SQL 语句
        for _u in _users:
            for _l in _level:
                for _e  in _ens:
                    _funcs.append(
                        func.sum(case(whens=[(and_(searchKeyWord.first_name == _u, searchKeyWord.number == _l, searchKeyWord.en == _e), 1)],else_=0)).label(_u + '_' + str(_l) + '_' + _e),
                    )

        

        # 查询执行组合 SQL 语句
        qs = db.query(
            func.count().label("total"),
            *_funcs,
        ).filter(searchKeyWord.created_at.between(_d + ' 00:00:00', _d + ' 23:59:59')).group_by('created_at')

        _results = [dict(zip(result.keys(), result)) for result in qs.all()]
        

        # 计算每个用户对应总共的数据，并添加年月日时间
        counter = collections.Counter()
        for _result in _results:
            counter.update(_result)

        # # 再批量添加到字典内,并添加日期时间
        _dict.update(dict(counter))
        
        _dict['created_at'] = _d
        results.append(_dict)


        # 组合成我们想要的数据
        _k1 = 'created_at'
        _k2 = 'users'
        _k3 = 'total'
        _k4 = 'username'
        _k5 = 'level'
        _k6 = 'count'
        _k7 = 'type'

        
        
        for _u in _users:
            for _d in results:
                _res = {}
                _res.update({_d[_k1]: {_k2: [], _k3: 0}})
                for _l in _level:
                    for _e in _ens:
                        _res[_d[_k1]][_k2].append({_k4: _u, _k5: _l, _k6: int(_d[_u + '_' + str(_l) + '_' + _e]), _k1: _d[_k1], _k7: _e})

                _res[_d[_k1]][_k3] = _d[_k3]
                res.append(_res) 
        return res


    async def get_count_today(self, db):
        # 获取今天日期
        _today  = await self.asy_get_today()

        # 获取关键词汇总用户
        _users = await self.asy_get_keyword_user(db, _today)

        # 获取关键词汇总排名序号
        _level = await self.asy_get_keyword_number(db, _today)

        # 获取关键词汇总所有类型
        _ens   = await self.asy_get_keyword_en(db, _today)
        

        # 获取当日统计数据
        _res = await self.asy_get_res(db, _today, _users, _level, _ens)



        resNew = self.modify_data("users", _res)
        db_data = self.modify_to_db(resNew)
        return db_data



services = Services()