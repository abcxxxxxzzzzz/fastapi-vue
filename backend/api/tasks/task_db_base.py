from api.exts.init_database import SessionLocal

def getDb():
    db = SessionLocal()
    return db



db = getDb()