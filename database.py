import sqlalchemy
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import settings

__author__ = 'hughson.simon@gmail.com'

engine = sqlalchemy.create_engine(
    'postgresql+psycopg2://%s:%s@%s/%s' %
    (settings.DB['user'],
     settings.DB['password'],
     settings.DB['host'],
     settings.DB['database']),
    echo=settings.DEBUG,
    pool_recycle=7200,
    pool_size=10)
try:
    db_session = scoped_session(sessionmaker(bind=engine))
# may need more exceptions here (or trap all)
except sqlalchemy.exc.OperationalError:
    db_session.rollback()
    engine = sqlalchemy.create_engine(
        'postgresql+psycopg2://%s:%s@%s/%s' %
        (settings.DB['user'],
         settings.DB['password'],
         settings.DB['host'],
         settings.DB['database']),
        echo=settings.DEBUG,
        pool_recycle=7200,
        pool_size=10)
    db_session = scoped_session(sessionmaker(
        bind=engine))  # replace your connection

Base = declarative_base()
Base.query = db_session.query_property()

