import xlwt
from typing import List,Dict,Optional
import uuid
import pathlib
from api.configs.config import global_settings
from api.utils import get_today
from .task_db_base import db
from api.models import taskRecord
from fastapi.encoders import jsonable_encoder
from api.utils import get_progress, get_today
from sqlalchemy.sql import and_


def get_pro(path, task_name, current_user, oneField: Optional[str] = None, oneValue: Optional[any] = None, filters=[],model=None, join_model=None, field: Optional[Dict] = None, update: Optional[Dict] = None, ConditionDelete: Optional[bool] = None, ConditionUpdate: Optional[bool] = None):
    _task = taskRecord(path=path,  task_name=task_name, progress=0, first_name=current_user)
    db.add(_task)
    db.commit()

    # 判断是否链表查询
    if join_model:
        total = db.query(model).join(join_model).filter(*filters).count()
    else:
        total = db.query(model).filter(*filters).count()

    # 判断是否执行的删除动作
    if ConditionDelete:
        ToDelete(path=path, current_user=current_user, total=total, filters=filters, model=model, join_model=join_model)

    elif ConditionUpdate:
        ToUpdate(path=path, current_user=current_user, total=total, filters=filters, model=model, join_model=join_model, oneField=oneField, oneValue=oneValue)
    else:
        # next_cmd = (datetime.now() + timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
        # Schedule.add_job(ToExcel, 'date',  run_date=next_cmd, misfire_grace_time=3600, args=[path,  current_user, field, update,total, filters])
        ToExcel(path=path, current_user=current_user,field=field, update=update, total=total, filters=filters, model=model, join_model=join_model)



def ToExcel(path:str, current_user:str, field: Dict,  update: Optional[Dict] = None, total: Optional[int] = 0, filters: Optional[List] = [], model: Optional[any] =None, join_model: Optional[any] = None):

    '''
        data: 数据库数据对象转换的列表：例如: [{},{}]
        field: 数据映射字段 key-value: 例如: {"first": 1 , "last": 2}
    '''
    

    db_field = list(field.keys())    # 数据库对应表列字段
    zh_field = list(field.values())  # 中文字段



    _ws = xlwt.Workbook(encoding='utf-8')

    # 定义表文件内 sheet 名字
    _p = 0
    _sheet = 1
    _skip = 1
    while 0 > -1:
        # # 如果数据取完则暂停
        # if _p == total:
        #     break

        # 设置每次从数据库取数据的数量
        _limit = 65535
        if join_model:
            _query = db.query(model).join(join_model).order_by(model.id.asc()).filter(*filters).offset((_skip-1)*_limit).limit(_limit)
        else:
            _query = db.query(model).filter(*filters).order_by(model.id.asc()).offset((_skip-1)*_limit).limit(_limit)
        _count = _query.count()
        if _count == 0:
            break

        data = jsonable_encoder(_query.all())

        # print(data)

        # 1、表头标题信息写入, 索引从 0 开始
        _st = _ws.add_sheet(f'表{_sheet}')
        # for index, value in enumerate(field):
        for index, value in enumerate(zh_field):
            _st.write(0, index, value)

        # 2、从第一行写入数据
        excelLine = 1
        for _d in data:
            for _i, _v in enumerate(db_field):
                # print(_d[_v])
                if update and _v in update and isinstance(_d[_v], list):
                    if _d[_v]:
                        _st.write(excelLine, _i, str(_d[_v][0][update[_v][0]]))
                    else:
                        _st.write(excelLine, _i, '')

                elif update and _v in update and  isinstance(_d[_v], dict):
                    if _d[_v]:
                        _st.write(excelLine, _i, str(_d[_v][update[_v][0]]))
                    else:
                        _st.write(excelLine, _i, '')

                # elif update and _v in update and isinstance(str(_d[_v]), dict):
                #     _st.write(excelLine, _i, update[_v][str(_d[_v])])
                else:
                    _st.write(excelLine, _i, str(_d[_v]).replace('\t','').replace('\n', '').replace(' ',''))
            excelLine += 1


        _p = _p + _count
        progress = get_progress(_p, total)
        is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
        is_exist.progress    = progress
        is_exist.updated_at  = get_today(hms=True)
        db.commit()

        print(progress)

        # 如果从数据库里取出的数据小于 步长数据，则暂停
        if _count < _limit or int(float(progress)) >= 100:
            break
       
        _skip = _skip + 1
        _sheet = _sheet + 1

    # 保存到服务器方式
    _saveName = str(uuid.uuid1()) + ".xlsx"
    _path = pathlib.Path(global_settings.down_name + '/' + get_today())
    if not _path.exists():
        _path.mkdir()

    _savePath = _path.joinpath(_saveName)
    _ws.save(_savePath)


    is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
    is_exist.description = str(_savePath)
    is_exist.updated_at  = get_today(hms=True)
    db.commit()

    # return FileResponse(
    #         _saveName,
    #         filename=_saveName,
    #         background=BackgroundTask(lambda: os.remove(str(_savePath))),
    #     )
    # return _savePath

    # 直接二进制的方法返回
    # _output = BytesIO()
    # _ws.save(_output)
    # _output.seek(0)
    # resp = make_response(output.getvalue())
    # filename = time.strftime("%Y-%m-%d", time.localtime())
    # basename = f'{filename}.xlsx'
    # # 转码，支持中文名称
    # resp.headers["Content-Disposition"] = f"attachment; filename={basename}"
    # resp.headers['Content-Type'] = 'application/vnd.ms-excel'
    # resp.headers["Cache-Control"] = "no_store"
    # return resp



def ToDelete(path:str, current_user:str, total: Optional[int] = 0, filters: Optional[List] = [], model: Optional[any] =None, join_model: Optional[any] = None):

    '''
        条件删除
    '''


    _p = 0
    _skip = 1
    while 0 > -1:
        _limit = 65535
        if join_model:
            _query = db.query(model).join(join_model).order_by(model.id.asc()).filter(*filters).offset((_skip-1)*_limit).limit(_limit)
        else:
            _query = db.query(model).filter(*filters).order_by(model.id.asc()).offset((_skip-1)*_limit).limit(_limit)
        _count = _query.count()
        if _count == 0:
            break


        for _q in _query.all():
            db.delete(_q)
        db.commit()

        _p = _p + _count
        progress = get_progress(_p, total)
        is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
        is_exist.progress    = progress
        is_exist.updated_at  = get_today(hms=True)
        db.commit()


        # 如果从数据库里取出的数据小于 步长数据，则暂停
        if _count < _limit or int(float(progress)) >= 100:
            break
       
        _skip = _skip + 1




    is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
    is_exist.description  = total
    is_exist.updated_at  = get_today(hms=True)
    db.commit()





def ToUpdate(path:str, current_user:str, oneField: str, oneValue: any, total: Optional[int] = 0, filters: Optional[List] = [], model: Optional[any] =None, join_model: Optional[any] = None):

    '''
        条件更新
    '''



    _p = 0
    _skip = 1
    while 0 > -1:
        _limit = 65535
        if join_model:
            _query = db.query(model).join(join_model).order_by(model.id.asc()).filter(*filters).offset((_skip-1)*_limit).limit(_limit)
        else:
            _query = db.query(model).filter(*filters).order_by(model.id.asc()).offset((_skip-1)*_limit).limit(_limit)
        _count = _query.count()
        if _count == 0:
            break


        for _q in _query.all():
            is_exist = getattr(_q, oneField, None)
           
            if is_exist is not None:
                setattr(_q, oneField, oneValue) if oneValue is not None else None
        db.commit()

        _p = _p + _count
        progress = get_progress(_p, total)
        is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
        is_exist.progress    = progress
        is_exist.updated_at  = get_today(hms=True)
        db.commit()


        # 如果从数据库里取出的数据小于 步长数据，则暂停
        if _count < _limit or int(float(progress)) >= 100:
            break
       
        _skip = _skip + 1




    is_exist = db.query(taskRecord).filter(and_(taskRecord.path==path, taskRecord.first_name==current_user)).first()
    is_exist.description  = total
    is_exist.updated_at  = get_today(hms=True)
    db.commit()

