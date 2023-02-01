from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
#import psycopg2
#from time import sleep

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<databasename>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#dbuser = "postgres"
#dbpassword = "Lazio1900"
#dbhost = "localhost"
#dbname = "fastapi"

#while(True):
#    try:
        #Connect to an existing database
#        conn = psycopg2.connect(f"dbname={dbname} user={dbuser} password={dbpassword} host={dbhost}")
#        cursor = conn.cursor()
#        print("Connection with database create successfully")
#        break
#    except Exception as error:
#        print("Connection to database failed")
#        print(f"Error: {error}")
#        sleep(2)

#Open a cursor to perform database operations
#cur = conn.cursor()