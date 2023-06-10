
from api.models import Tag,MemberProfile,taskRecord
from sqlalchemy.sql import and_
from api.utils import get_today
from api.utils import get_progress, get_today
from api.tasks.task_db_base import db


def import_excel(gid, path, current_user, data):

    _task = taskRecord(path=path,  task_name='会员信息导入', progress=0, first_name=current_user)
    db.add(_task)
    db.commit()



    query_tags      = db.query(Tag).all()

    if data:
        if len(data) > 20:
            setp = int(len(data) / 20)
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
            inset_data  = []
            update_data = []
            temp_update = {}



            if ds:
                for d in ds:
                    d['owner']      = str(d.get('owner','')).replace(" ","")
                    d['account']    = str(d.get('account','')).replace(" ","")
                    d['account_id'] = str(d.get('account_id','')).replace(" ","")
                    _tags           = str(d.get('tags', '').replace(" ",""))
                    tags            = []

                    for t in query_tags:
                        if t.name == _tags:
                            tags.append(t)

                    d['tags'] = tags


                # 组合数据
                _dsUser      = list(map(lambda x:x['account'], ds))
                _isInDbQuery = db.query(MemberProfile).filter(and_(MemberProfile.owner_id==gid, MemberProfile.account.in_(_dsUser))).all()   # 从数据库查询数据
                _isInDbList  = list(map(lambda x:x.account, _isInDbQuery))                                                 # 组合从数据库拿到的数据
                # _noInDb      = list(set(_dsUser).difference(set(_isInDbList)))                                           # 筛选不存在的数据


                for d in ds:
                    _owner       = d['owner']
                    _account     = d['account']
                    _account_id  = d['account']
                    _tags        = d['tags']

                    if _owner and _account and _account not in _isInDbList:
                        inset_data.append(
                                MemberProfile(
                                    owner_id    = gid,
                                    code        = d.get('code',None),
                                    account     = _account,
                                    account_id  = _account_id,
                                    realname    = d.get('realname', None),
                                    iphone_num  = d.get('iphone_num', None),
                                    contact     = d.get('contact', None),
                                    bank_number = d.get('bank_number', None),
                                    tags        = _tags,
                                    description = d.get('description', None),
                                    first_name  = current_user,
                            )
                        )
                        
                        insert_total += 1 
                    elif _owner and _account and _account in _isInDbList:
                        update_data.append(d)
                        temp_update.update({_account: d})
                        update_total += 1
                    else:
                        error.append(_account)
                        error_total += 1

                if update_data:
                    _isInDbUp = db.query(MemberProfile).filter(and_(MemberProfile.owner_id==gid, MemberProfile.account.in_(temp_update.keys()))).all()
                    for _isIn in _isInDbUp:
                        _isIn.code        = temp_update[_isIn.account].get('code',None)
                        _isIn.account_id  = temp_update[_isIn.account].get('account_id',None)
                        _isIn.realname    = temp_update[_isIn.account].get('realname', None)
                        _isIn.contact     = temp_update[_isIn.account].get('contact', None)
                        _isIn.bank_number = temp_update[_isIn.account].get('bank_number', None)
                        _isIn.iphone_num  = temp_update[_isIn.account].get('iphone_num', None)
                        # _isIn.tags        = d.get('tags', [])
                        # _isIn.description = d.get('description', None)
                        _isIn.last_name   = current_user
                        _isIn.updated_at  = get_today(hms=True)

                    # 提交更新
                    try:
                        db.commit()
                    except Exception as e:
                        update_total = update_total - len(update_data)
                        error_total  = error_total + len(update_data)
                        for i in update_data:
                            error.append(i['account'])

                # 提交插入
                try:
                        
                    if inset_data:
                        # db.execute(
                        #     MemberProfile.__table__.insert(),
                        #     inset_data
                        # )
                        # s = SessionLocal()
                        db.bulk_save_objects(inset_data)
                    db.commit()
                except Exception as e:
                    if inset_data:
                        for i in inset_data:
                            error.append(i.account)

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
