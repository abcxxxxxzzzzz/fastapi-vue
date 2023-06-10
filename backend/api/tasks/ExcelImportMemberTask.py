from sqlalchemy.orm import sessionmaker
from api.exts.init_database import engine
from api.models import Member,Group,taskRecord
from sqlalchemy.sql import and_
from api.utils import get_progress, get_today
from datetime import datetime , timedelta
from fastapi.encoders import jsonable_encoder
from .task_db_base import db
import time

def change_dateime(val):
        try:
            UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
            utc_time1 = datetime.strptime(val, UTC_FORMAT)
            local_date = utc_time1 + timedelta(hours=8)
            return datetime.strftime(local_date ,'%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return val




# 加彩金任务
def excel_import_member(gid, path, current_user, data):
        
        # 提交一次需要重新获取一次  session 链接， 不然无法再次提交
        

        # Session = sessionmaker(engine)
        # with engine.connect() as connection:
        #     with Session(bind=connection) as db:
        _task = taskRecord(path=path,  task_name='会员资料导入', progress=0, first_name=current_user)
        db.add(_task)
        db.commit()




        # 从数据库当中获取所有的组、标签
        # query_groups  = db.query(Group).filter(Group.id==gid).first()
        # query_groups_members_list = list(map(lambda x:x.get('username',None), jsonable_encoder(query_groups.members.all(), include=['username', 'id'])))



        if data:
            # print(data)
            # 切片步数
            if len(data) > 20:
                setp = int(len(data) / 20)
            else:
                setp = 4

            
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

                for d in ds:
                    d['owner'] = str(d.get('owner','')).replace(" ","")
                    d['username'] = str(d.get('username','')).replace(" ","")
                    d['channel_code'] = str(d.get('channel_code','')).replace(" ","")


                if ds:
                    _dsUser      = list(map(lambda x:x['username'], ds))                                             # 去除切片数据
                    _isInDbQuery = db.query(Member).filter(and_(Member.owner_id==gid, Member.username.in_(_dsUser))).all()   # 从数据库查询数据
                    _isInDbList  = list(map(lambda x:x.username, _isInDbQuery))                                              # 组合从数据库拿到的数据
                    _noInDb      = list(set(_dsUser).difference(set(_isInDbList)))                                           # 筛选不存在的数据

                    # 切片组合数据
                    for d in ds:
                        _owner         = d['owner']
                        _username      = d['username']
                        _channel_code  = d['channel_code']

                        # 如果添加的数据存在部门和账号
                        if _owner and _username:
                                d.pop('owner')
                                d['owner_id']   = gid
                                d['first_name'] = current_user
                                

                                # 存在则更新数据
                                # if _username in query_groups_members_list:
                                if _username in _isInDbList:
                                    # print(_username, query_groups_members_list)
                                    d['channel_code'] = _channel_code
                                    d['username'] = _username
                                    update_data.append(d)
                                    update_total += 1

                                # 不存在则添加数据
                                elif _username in _noInDb:
                                    d['channel_code'] = _channel_code
                                    inset_data.append(d)
                                    insert_total += 1
                                else:
                                    error.append(_username)
                                    error_total += 1



                    if update_data:


                        update_date_dict = {}
                        for da in update_data:
                            update_date_dict[da['username']] = da


                        exists_obj_update = db.query(Member).filter(Member.username.in_(list(update_date_dict.keys()))).all()
                        for p in exists_obj_update:
                            p.total_in_money               = update_date_dict[p.username].get('total_in_money', 0)
                            p.total_out_money              = update_date_dict[p.username].get('total_out_money', 0)
                            p.total_before_two_in_money    = update_date_dict[p.username].get('total_before_two_in_money', 0)
                            p.total_before_two_throw_money = update_date_dict[p.username].get('total_before_two_throw_money', 0)
                            p.total_before_two_out_money   = update_date_dict[p.username].get('total_before_two_out_money', 0)
                            p.total_before_two_wax_money   = update_date_dict[p.username].get('total_before_two_in_money', 0) - update_date_dict[p.username].get('total_before_two_out_money', 0)
                            p.total_wax_money              = update_date_dict[p.username].get('total_in_money', 0) - update_date_dict[p.username].get('total_out_money', 0)
                            p.register_ip                  = update_date_dict[p.username].get('register_ip','')
                            p.last_login_ip                = update_date_dict[p.username].get('last_login_ip','')
                            p.last_name                    = current_user
                            p.updated_at                   = get_today(hms=True)
                            p.register_at                  = change_dateime(update_date_dict[p.username].get('_register_at', ''))
                            p.last_login_at                = change_dateime(update_date_dict[p.username].get('_last_login_at', ''))

                        try:
                            db.commit()
                        except Exception as e:
                            update_total = update_total - len(update_data)
                            error_total  = error_total + len(update_data)
                            for i in update_data:
                                error.append(i['username'])


                    
                    try:
                            
                        if inset_data:
                            db.execute(
                                Member.__table__.insert(),
                                inset_data
                            )
                        db.commit()
                    except Exception as e:
                        if inset_data:
                            for i in inset_data:
                                error.append(i['username'])

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
                    
                    # time.sleep(1)
                else:
                    is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
                    is_exist.progress = 100
                    is_exist.updated_at  = get_today(hms=True)
                    db.commit()
                    break


                        