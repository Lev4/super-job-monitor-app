import logging
from dbsrc import DataAccessLayer, Vacancy, VacancyMessage
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


def get_vacancies():
    dal = DataAccessLayer(conn_string)
    dal.connect()
    list_of_vacs = dal.session.query(Vacancy.vacid).all()
    dal.session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]
    return list_of_vacs


def get_first_vacancy_id():
    dal = DataAccessLayer(conn_string)
    dal.connect()
    list_of_vacs = dal.session.query(Vacancy.vacid).first()
    dal.session.commit()
    vacancy_id = list_of_vacs[0]

    return vacancy_id


def get_vacancies_by_key_words():
    dal = DataAccessLayer(conn_string)
    dal.connect()
    list_of_vacs = dal.session.query(Vacancy.vacid).filter(Vacancy.vactitle.op('~')(r"python|Руководитель")).all()
    dal.session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]

    return list_of_vacs


def get_vacancy_obj(vac_id):
    dal = DataAccessLayer(conn_string)
    dal.connect()
    vobj = dal.session.query(Vacancy).filter(Vacancy.vacid == vac_id).first()
    dal.session.commit()
    return vobj



def previous_current_next(iterable):
    """Создает итератор который выдает таплы (предыдущий, текущий, следующий)

    Если нет значения, то значения предыдущего или следующего, то возвращает None

    """
    iterable = iter(iterable)
    prv = None
    cur = next(iterable)
    try:
        while True:
            nxt = next(iterable)
            yield prv, cur, nxt
            prv = cur
            cur = nxt
    except StopIteration:
        yield prv, cur, None


def add_user_to_db():
    pass


def update_user_data_in_db():
    pass


def delete_user_in_db():
    pass
