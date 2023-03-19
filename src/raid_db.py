
import os
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()


class FrameworkMod(Base):
    """
    Класс для работы с Издателем
    """
    __tablename__ = "framework"

    pk = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False, unique=True)
    language = sq.Column(sq.String(length=40), nullable=False)


def create_tables(engine):
    """
    Пересооздаёт все таблицы в БД
    :param engine:
    :return:
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_dsn():
    """
    Получает параметры подлключения к БД из переменных среды
    :return:
    Строку с DSN
    """
    if {"PSTGRS_USER", "PSTGRS_PASSWD", "PSTGRS_DB", "PSTGRS_HOSTNAME"} <= os.environ.keys():
        return f'postgresql://{os.environ["PSTGRS_USER"]}:{os.environ["PSTGRS_PASSWD"]}' + \
                f'@{os.environ["PSTGRS_HOSTNAME"]}:5432/{os.environ["PSTGRS_DB"]}'
    else:
        return None


def get_shops_by_pub(session, pub):
    """
    Возвращает множество названий магазинов продающих определённого издателя
    :param pub: Имя издателя
    :return: Множество названий магазинов
    """
    q = session.query(
        Publisher, Book, Stock, Shop
    ).filter(
        Publisher.id == Book.id_publisher
    ).filter(
        Book.id == Stock.id_book
    ).filter(
        Shop.id == Stock.id_shop
    ).filter(
        Publisher.name == pub
    )

    result = set()
    for s in q.all(): result = result.union({s.Shop.name})
    return result


def connect_db():
    DSN = get_dsn()
    if not DSN:
        print("""
Необходимо задать параметры подключения к БД через переменные среды:
    PSTGRS_DB     - Имя базы данных
    PSTGRS_USER   - Имя пользователя
    PSTGRS_PASSWD - Пароль пользователя
    PSTGRS_HOSTNAME - Имя или адрес хоста
""")
        return
    return sq.create_engine(DSN)

    engine = sq.create_engine(DSN)
def create_db():

    engine = connect_db()
    if not engine: return

    create_tables(engine)
    engine.dispose()

def fill_db():
    engine = connect_db()
    if not engine:
        return

    Session = sessionmaker(bind=engine)
    session = Session()

    list_to_add = []

    list_to_add.append(FrameworkMod(pk=1, name="React", language="Javascript"))
    list_to_add.append(FrameworkMod(pk=2, name="Vue", language="Javascript"))
    list_to_add.append(FrameworkMod(pk=3, name="FastApi", language="Python"))
    list_to_add.append(FrameworkMod(pk=4, name="Laravel", language="PHP"))
    list_to_add.append(FrameworkMod(pk=5, name="Spring", language="Java"))


    session.add_all(list_to_add)
    session.commit()
    session.close()
    engine.dispose()
