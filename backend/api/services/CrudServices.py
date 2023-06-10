from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from api.utils import logger,get_today
from sqlalchemy.sql import text
from typing import Optional,List,Union
from api.models import SearchWeight

class CommaonCrud(object):

    
    # 列
    async def get_items(self, db: Session, 
                            model, 
                            join_model: Union[object, None] = None,
                            keyword_field: Optional[str]=None,  # 模糊搜索的关键词
                            paging: Optional[bool]=True,         # 是否分页,默认分页
                            params: Optional[str]={},           # 路径参数
                            # query_in: Optional[list] = [],      # in 包含参数
                            other_filter: Optional[list] = [],  # 其他过滤参数
                            order_enable: bool = False,
                            order_field: Optional[List] = [], # 默认创建时间字段
                            order_value: str = 'desc',         # 默认降序
                            *args, **data):
        
        # # 根据时间范围筛选
        # if time_field and start_time and end_time:
        #     filter.append(text(f'''{time_field} > "{start_time}" and {time_field} < "{end_time}"'''))
            

        from fastapi.encoders import jsonable_encoder


        # 判断是否链表查询
        if join_model:
            obj = db.query(model).join(join_model)
        else:
            obj = db.query(model)
        filters = []

        

        _params =  jsonable_encoder(params)
        # 如果有 in 包含参数
        if other_filter:
            for i in other_filter:
                filters.append(i)


        # 如果有路径参数
        if _params:
            for k, v in _params.items():
                # 过滤字段
                if getattr(model, k, None):
                    filters.append(text(f'''{k} = {v}'''))
                    continue
                # 模糊关键词，需传入关键词对应数据库字段
                if k == 'keyword' and v and keyword_field:
                    filters.append(text(f'''{keyword_field} like "%{v}%"'''))

            # 最后如果分页和未分页，默认分页
            if paging:
                skip = _params['skip']
                limit = _params['limit']
                query = obj.filter(*filters)

                


                try:
                    if order_enable and order_field:
                        return query.order_by(order_field[0]).offset((skip- 1)*limit).limit(limit).all(), query.count()
                    return query.order_by(model.id.desc()).offset((skip- 1)*limit).limit(limit).all(), query.count()

                    # return query.join(SearchWeight).filter(SearchWeight.en=='sex').order_by(model.id.desc()).offset((skip- 1)*limit).limit(limit).all(), query.count()
                except SQLAlchemyError as e:
                    logger.error(str(e))
                    raise HTTPException(status_code=400, detail='数据查询失败')
                except Exception as e:
                    logger.error(str(e))
                    raise HTTPException(status_code=500, detail='请联系管理员')
            else:
                query =  obj.filter(*filters).order_by(model.id.desc())

        else:
            # 否则查询全部
            # query.filter_by(*filter).order_by(text(f'''{order_field} {order_value}'''))
            query =  obj.filter(*filters).order_by(model.id.desc())

        # print(query.all().sort(key=lambda x: x.id, reverse=False))
        try:
            return query.all(), query.count()
        except SQLAlchemyError as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据查询失败')
        except Exception as e:
            print('这里错了？',e)
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')



    # 查
    async def show_item(self,db: Session, model, id):
        try:
            query = db.query(model).filter(model.id == id).first()
            if query:
                return query
            raise HTTPException(status_code=404, detail='未找到')
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据查询失败')
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')


    # 增
    async def create_item(self, db: Session, model, **data):
        try:
            query = model(**data)
            db.add(query)
            db.commit()
            db.refresh(query)
            return query
        except IntegrityError as e:
            db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='已存在')
        except SQLAlchemyError as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据添加失败')
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')
    # 删
    async def delele_item(self,db: Session, model, id, recover=False, last_name=False):
        query = db.query(model).filter(model.id == id)
        if not query.first():
            raise HTTPException(status_code=404, detail='未找到')
        
        try:
            if recover:
                if last_name:
                    query.update({'is_del': 1,'last_name': last_name, 'delete_at': get_today(hms=True)})
                else:
                    query.update({'is_del': 1,'delete_at': get_today(hms=True)})
            else:
                db.delete(query.first())

            db.commit()
            return True
        except IntegrityError as e:
            logger.error(str(e))
            raise HTTPException(status_code=403, detail='外键关联，无法删除，请先去除关联')
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据删除失败')
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')

    # 改
    async def update_item(self, db: Session,  model, id, **data):
        try:
            query = db.query(model).filter(model.id == id).first()
            if query:
                for var, value in data.items():
                    # print(var, value)
                    if isinstance(value, list):
                        setattr(query, var, value)
                    elif isinstance(value, str):
                        setattr(query, var, value) if value  else setattr(query, var, None)
                    elif isinstance(value, int):
                        setattr(query, var, value)
                    else:
                        # print(value)
                        # print(type(value))
                        setattr(query, var, value) if value   else None
                db.commit()
                db.refresh(query)
                return query
            raise HTTPException(status_code=404, detail='未找到')
        except IntegrityError as e:
            logger.error(str(e))
            raise HTTPException(status_code=403, detail='已存在，请检查')
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据更新失败')
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')

    # 改
    async def update_status_item(self, db: Session,  model, id, **data):
        try:
            query = db.query(model).filter(model.id == id).first()
            if query:
                for var, value in data.items():
                    setattr(query, var, value)
                db.commit()
                db.refresh(query)
                return query
            raise HTTPException(status_code=404, detail='未找到')
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据更新失败')
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')


    # 批量删除，但不是真正的删除
    async def multi_delete(self, db: Session,  model, ids=[], multi_delete=False, last_name=False):
        if not ids:
            raise HTTPException(status_code=400, detail='无数据删除')
        try:
            query = db.query(model).filter(model.id.in_(ids))
            if multi_delete: # 彻底删除
                for i in query.all():
                    db.delete(i)
            elif last_name:
                query.update({'is_del': 1,'last_name': last_name, 'delete_at': get_today(hms=True)})
            else:
                query.update({'is_del': 1,'delete_at': get_today(hms=True)})
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据删除失败')
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')

    # 批量回收
    async def recover_delete(self, db: Session,  model, ids=[], last_name=False):
        if not ids:
            raise HTTPException(status_code=400, detail='无数据还原')
        try:
            query = db.query(model).filter(model.id.in_(ids))
            if last_name:
                query.update({'is_del': 0,'last_name': last_name})
            else:
                query.update({'is_del': 0})
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据还原失败')
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')

    # 批量清空回收站
    async def clear_delete(self, db: Session,  model, ids=[], last_name=False):
        if not ids:
            raise HTTPException(status_code=400, detail='无数据清空')
        try:
            query = db.query(model).filter(model.id.in_(ids)).filter(model.is_del==1).all()
            for i in query:
                db.delete(i)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据清空失败')
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')


    # 分组
    async def group_by(self, db: Session,  model, _group_by):

        try:
            query = db.query(model).group_by(_group_by).having(_group_by != None).all()
            return query
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=400, detail='数据查询分组失败')
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail='请联系管理员')



Crud = CommaonCrud()



# async def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# async def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# async def update_user(db: Session, user_id: int, user: models.UserUpdate):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if db_user:
#         for var, value in vars(user).items():
#             setattr(db_user, var, value) if value else None
#         await db.commit()
#         await db.refresh(db_user)
#     return db_user


# async def delete_user(db: Session, user_id: int):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if db_user:
#         db.delete(db_user)
#         await db.commit()
#     return db_user


# async def create_role(db: Session, role: models.RoleCreate):
#     db_role = models.Role(name=role.name
