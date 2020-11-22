from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_NAME = 'todo.db'
ENGINE_STR = 'sqlite:///{}?check_same_thread=False'

engine = create_engine(ENGINE_STR.format(DB_NAME))
Session = sessionmaker(bind=engine)
Base = declarative_base()
