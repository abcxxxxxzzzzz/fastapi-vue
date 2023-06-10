from api.models.admin_user import *










# from sqlalchemy import create_engine
# from databases import Database
# from .db_metadata import metadata



# DATABASE_URL = "sqlite:///./fastapi.db"                               # SQLITE
# # DATABASE_URL = "mysql://user:password@localhost/db?charset=utf8mb4" # MYSQL
# # DATABASE_URL = "postgresql://user:password@postgresserver/db"       # POSTGRESQL

# database = Database(DATABASE_URL)

# # engine = create_engine(DATABASE_URL)                                # MYSQL 引擎 || POSTGRESQL 引擎
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})     # SQLITE

# metadata.create_all(engine)





# async def startup_event():
#     await database.connect()

# async def shutdown_event():
#     await database.disconnect()

