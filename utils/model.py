from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Model():
    def __init__(self):
        connection_str = "postgresql://postgres:0000@localhost:5432/PyQt_app"

        try:
            self.engine = create_engine(connection_str)
            self.engine.connect()
            self.Session = sessionmaker(bind=self.engine)
            print("Соединение установлено успешно.")
        except OperationalError as e:
            print("Не удалось установить соединение. Ошибка:", e)
            raise

    def create_all_table(self):
        Base.metadata.create_all(self.engine)


class Role(Base):

    __tablename__ = 'role'

    id_role = Column(Integer, primary_key=True)
    role_name = Column(String(50))

class Users(Base):

    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True)

    login = Column(String(100))
    password = Column(String(50))
    last_come = Column(DateTime())
    role_id = Column(Integer, ForeignKey('role.id_role'))
    role = relationship('Role')


