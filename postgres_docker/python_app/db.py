from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = None
try:
    from python_app.definitions import CON_URI
    engine = create_engine(CON_URI)
except:
    pass


Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

def commit_on_success(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        session.commit()
        return result
    return wrapper

