
import os
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()


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


class FrameworkMod(Base):
    """
    Класс для работы с Издателем
    """
    __tablename__ = "framework"

    pk = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False, unique=True)
    language = sq.Column(sq.String(length=40), nullable=False)


class RaidSession:
    """Класс для работы с БД"""

    def __init__(self, dsn):
        self.engine = None
        self.session = None
        self.dsn = dsn

    def create_tables(self):
        """
        Пересооздаёт все таблицы в БД
        :param engine:
        :return:
        """
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)


    def connect_db(self):
        self.engine = sq.create_engine(self.dsn)
        return self.engine

    def create_session(self):
        if not self.engine: self.connect_db()
        if self.engine:
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        return self.session

    def create_db(self):
        if not self.connect_db(): return False
        self.create_tables()
        self.engine.dispose()
        self.engine = None
        return True

    def fill_db(self):
        if not self.create_session(): return

        list_to_add = []

        list_to_add.append(FrameworkMod(pk=1, name="React", language="Javascript"))
        list_to_add.append(FrameworkMod(pk=2, name="Vue", language="Javascript"))
        list_to_add.append(FrameworkMod(pk=3, name="FastApi", language="Python"))
        list_to_add.append(FrameworkMod(pk=4, name="Laravel", language="PHP"))
        list_to_add.append(FrameworkMod(pk=5, name="Spring", language="Java"))

        self.session.add_all(list_to_add)
        self.session.commit()

        self.session.close()
        self.session = None
        self.engine.dispose()
        self.engine = None


    def get_frameworks(self):
        """
        Возвращает содержимое таблицы framework
        :param:
        :return:
        """
        if not self.session:
            self.create_session()

        q = self.session.query(
            FrameworkMod
        )

        result = []
        for s in q.all(): result.append(
            {"pk": s.pk,
             "name": s.name,
             "language": s.language})
        return result

