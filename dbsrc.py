import datetime
import logging

from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# conn_string = f'postgresql+psycopg2://'
# conn_string = f'postgresql://'
# conn_string += f'{dbconfig.DATABASE_USER}:{dbconfig.DATABASE_PASS}'
# conn_string += f'@{dbconfig.DATABASE_HOST}:{dbconfig.DATABASE_PORT}/{dbconfig.DATABASE_NAME}'

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable = False, unique = True, primary_key = True, autoincrement = True)
    created_at = Column(TIMESTAMP, nullable = False, default = datetime.datetime.now())
    updated_at = Column(TIMESTAMP, nullable = False, default = datetime.datetime.now(),
                        onupdate = datetime.datetime.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Vacancy(BaseModel):
    """ Модель данных для таблицы вакансий """

    __tablename__ = 'vacancy'

    vacid = Column(VARCHAR())
    vactitle = Column(VARCHAR(255))
    vacdescription = Column(VARCHAR())
    vacdate = Column(VARCHAR(255))
    vacstatus = Column(VARCHAR(100))

    def __init__(self, vacid, vactitle, vacdescription, vacdate, vacstatus):
        self.vacid = vacid
        self.vactitle = vactitle
        self.vacdescription = vacdescription
        self.vacdate = vacdate
        self.vacstatus = vacstatus

    def __repr__(self):
        return f'{self.vactitle} {self.vacdescription}'


class DataAccessLayer:
    """Подключение к базе данных. Сессия"""

    def __init__(self, connection_string):
        self.engine = None
        self.session = None
        self.Session = None
        self.conn_string = connection_string

    def connect(self):
        logging.info(f"Подключаюсь к БД")
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind = self.engine)
        self.session = self.Session()
