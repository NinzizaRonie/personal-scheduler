from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
try: # connection to database 
    my_conn = create_engine("sqlite:///schedules.db")
except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
