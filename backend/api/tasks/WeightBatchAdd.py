
from api.utils import logger,get_today,get_domain
from api.models import Weight,SearchWeight,taskRecord
from sqlalchemy import and_
from .task_db_base import db
from api.utils import get_progress, get_today


def batch_add(path, data, _type, current_user):
    _task = taskRecord(path=path,  task_name='批量添加权重域名', progress=0, first_name=current_user)
    db.add(_task)
    db.commit()

    new_data = []

    # 先组合数据
    if isinstance(data, str):
        batchContent = data.split('\n')
        for b in batchContent:
            if b:
                name = get_domain(b)
                new_data.append(name)
                # o = db.query(Weight).filter(and_(Weight.name==name, Weight.type==_type)).first()
                # if not o:
                #     obj = Weight(name=name, type=_type)
                #     db.add(obj)
                #     db.commit()
                #     db.refresh(obj)
    if new_data:
        # print(data)
        # 切片步数
        if len(new_data) > 20:
            setp = int(len(new_data) / 20)
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
            ds = new_data[n:n+setp]
            inset_data = []

            if ds:
                _isInDbQuery = db.query(Weight).filter(and_(Weight.name.in_(ds), Weight.type==_type)).all()
                _isInDbList  = list(map(lambda x:x.name, _isInDbQuery)) 
                _noInDb      = list(set(ds).difference(set(_isInDbList)))
                error_total = error_total + len(_isInDbList)
                insert_total = insert_total + len(_noInDb)


                # 把不存在的批量添加到数据库
                if _noInDb:
                    for d in _noInDb:
                        inset_data.append({'name': d, 'type': _type})
             
                try:
                    if inset_data:
                        db.execute(
                            Weight.__table__.insert(),
                            inset_data
                        )
                        db.commit()
                        
                except Exception as e:
                    if inset_data:
                        for i in inset_data:
                            error.append(i['name'])

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

                progress = get_progress(n, len(new_data))
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
