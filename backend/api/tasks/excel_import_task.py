from sqlalchemy.orm import sessionmaker
from api.exts.init_database import engine
from api.models import Member,Group,MemberCaiJinSource,MemberCaiJin,taskRecord
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import and_
import decimal
from api.utils import get_progress,get_today
from .task_db_base import db


# @lock('asdfasdf497987')
# async def myTest(path , db, current_user, item):
#     # global Schedule
#     Schedule.add_job(excel_import, 'date',  run_date='2023-05-01 14:25:00', args=[path , db, current_user, item])




# 加彩金任务
def excel_import_caijin(gid,  path,current_user, data):

        # Session = sessionmaker(engine)
        # with engine.connect() as connection:
        #     with Session(bind=connection) as db:

        try:
            _task = taskRecord(path=path,  task_name='彩金批量导入', progress=0, first_name=current_user)
            db.add(_task)
            db.commit()
            
            # 从数据库当中获取所有彩金类型
            query_source = db.query(MemberCaiJinSource).all()
            query_sources_dict = {}
            for q in query_source:
                query_sources_dict[q.name] = q.id

            # query_groups_members_list = list(map(lambda x:x.get('username',None), jsonable_encoder(query_groups.members.all(), include=['username', 'id'])))


    



            if data:
                if len(data) > 10:
                    setp = int(len(data) / 10)
                else:
                    setp = 2

                # 进度条设置
                n = 0
                insert_total = 0
                update_total = 0
                error_total  = 0
                error        = []


                while n > -1:
                    # 切片设置
                    ds = data[n:n+setp]
                    inset_data = []
                    update_data = []
                    temp_dict = {}

                    for d in ds:
                        d['username'] = str(d.get('username', '')).replace(" ","")
                        d['source'] = str(d.get('source','')).replace(" ","")
                        d['money'] = str(d.get('money','')).replace(" ","")
                        first_name = current_user



                    if ds:
                        query_usernames_dict = {}
                        _dsUser      = list(map(lambda x:x['username'], ds))                                             # 去除切片数据
                        _isInDbQuery = db.query(Member).filter(and_(Member.owner_id==gid, Member.username.in_(_dsUser))).all()   # 从数据库查询数据
                        # _isInDbList  = list(map(lambda x:x.username, _isInDbQuery))                                              # 组合从数据库拿到的数据
                        # _noInDb      = list(set(_dsUser).difference(set(_isInDbList)))  

                        for q in _isInDbQuery:
                            query_usernames_dict[q.username] = q.id

                        # 切片组合数据
                        for d in ds:
                            # username = str(d.get('username', '')).replace(" ","")
                            # source = str(d.get('source','')).replace(" ","")
                            # money = str(d.get('money','')).replace(" ","")
                            # first_name = current_user

                            try:
                                _c = {}
                                _c['member_id']    = query_usernames_dict[d['username']]
                                _c['source_id']    = query_sources_dict[d['source']]
                                _c['money']        = decimal.Decimal(d['money'])
                                _c['description']  = d.get('description',None)
                                _c['first_name']   = first_name
                                inset_data.append(_c)
                                insert_total += 1

                                # 临时存储，方便批量添加失败查询
                                temp_dict[query_usernames_dict[d['username']]] = d['username']
                            except:
                                error.append(d['username'])
                                error_total += 1



                        # 批量添加进去                    
                        try:
                            if inset_data:
                                db.execute(
                                    MemberCaiJin.__table__.insert(),
                                    inset_data
                                )
                                db.commit()
                        except Exception as e:
                            for i in inset_data:
                                error.append(temp_dict[i['member_id']])

                            error_total = error_total + len(inset_data)
                            insert_total = insert_total - len(inset_data)
                            from api.utils.logs import logger
                            logger.error(str(e))





                        # 获取进度
                        description = {
                            'error': error[:100],
                            'insert_total': insert_total,
                            'update_total': update_total,
                            'error_total': error_total,
                        }

                        progress = get_progress(n, len(data))
                        is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
                        is_exist.progress    = progress
                        is_exist.description = str(description)
                        is_exist.updated_at  = get_today(hms=True)
                        db.commit()

                        n += setp

                    else:

                        is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
                        is_exist.progress = 100
                        is_exist.updated_at  = get_today(hms=True)
                        db.commit()
                        break

        except:
                is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
                is_exist.progress = 100
                is_exist.updated_at  = get_today(hms=True)
                db.commit()
        finally:
            db.close()


                # path        = path

                # description = {
                #             'error': str(errData),
                #             'insert_total': len(newData),
                #             'update_total': 0,
                #             'error_total':len(errData),
                #         }


                # if newData:

                    
                #     # 切片步数
                #     if len(newData) > 20:
                #         setp = int(len(newData) / 20)
                #     else:
                #         setp = 2
                    

                #     # 进度条设置
                #     n = 0

                #     while n > -1:
                #         d = newData[n:n+setp]
                #         inset_data = []
                #         if d:
                #             try:

                #                 for _i in d:

                #                 # 最后批量添加验证过的数据
                #                 db.execute(
                #                     MemberCaiJin.__table__.insert(),
                #                     inset_data
                #                 )


                #                 # 彩金数量相加
                #                 member_ids = list(map(lambda x:x['member_id'], inset_data))
                #                 _show = db.query(Member).filter(Member.id.in_(member_ids)).all()
                #                 if _show:
                #                     for _s in _show:
                #                         for _insert in inset_data:
                #                             if int(_insert['member_id']) == int(_s.id):
                #                                 _s.total_caijin_money = _s.total_caijin_money + decimal.Decimal(_insert['money'])


                #                 # 获取进度
                #                 progress = get_progress(n, len(newData))
                #                 is_exist = db.query(taskRecord).filter(taskRecord.path==path).first()
                #                 is_exist.progress    = progress
                #                 is_exist.description = str(description)
                #                 is_exist.updated_at  = get_today(hms=True)
                #                 db.commit()
                #             except Exception as e:
                #                 db.rollback()
                #                 print(e)

                #             n += setp
                            
                #         else:

                #             # 循环之后最后设置 100%
                #             t_is_exist= db.query(taskRecord).filter(taskRecord.path==path).first()
                #             t_is_exist.progress = 100
                #             is_exist.updated_at  = get_today(hms=True)
                #             db.commit()
                #             break

                
                
                # else:
                #     is_exist = db.query(taskRecord).filter(taskRecord.path==path).first()
                #     is_exist.progress = 100
                #     is_exist.updated_at  = get_today(hms=True)
                #     db.commit()
                #     # pass