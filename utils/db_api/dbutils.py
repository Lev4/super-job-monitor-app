import logging
from dbsrc import DataAccessLayer, Vacancy
from data.config import conn_string
from sqlalchemy.exc import DBAPIError


def get_num_vacancies():
    dal = DataAccessLayer(conn_string)
    dal.connect()
    rows = dal.session.query(Vacancy).count()
    dal.session.commit()
    return rows

def get_num_vacancies_by_key_words():
    dal = DataAccessLayer(conn_string)
    dal.connect()
    list_of_vacs = dal.session.query(Vacancy.vacid).filter(Vacancy.vactitle.op('~')(r"python|Руководитель")).all()
    dal.session.commit()

    return len(list_of_vacs)


def get_num_vacancies_by_key_words():
    dal = DataAccessLayer(conn_string)
    dal.connect()
    list_of_vacs = dal.session.query(Vacancy.vacid).filter(Vacancy.vactitle.op('~')(r"python|Руководитель")).all()
    dal.session.commit()

    return len(list_of_vacs)

def get_vacancies_by_key_words():
    dal = DataAccessLayer(conn_string)
    dal.connect()
    list_of_vacs = dal.session.query(Vacancy.vacid).filter(Vacancy.vactitle.op('~')(r"python|Руководитель")).all()
    dal.session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]

    return list_of_vacs

def add_user_to_db():
    pass