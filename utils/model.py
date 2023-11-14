import PyQt5.QtSql
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from PyQt5.QtSql import QSqlQuery, QSqlDatabase, QSqlQueryModel
import sqlite3
import psycopg2
class Model:
    def __init__(self):
        # self.conn = sqlite3.connect('db_organisation.db')
        try:
            self.conn = psycopg2.connect(
                database='Organisation_taksPyqt',
                host='localhost',
                port='5432',
                user='postgres',
                password='0000'
            )
            print('Соединение успешно')
        except psycopg2.Error as e:
            print('Не удалось подлючиться ', e)
        try:
            self.db = QSqlDatabase.addDatabase('QPSQL')
            self.db.setDatabaseName('Organisation_taksPyqt')
            self.db.setUserName('postgres')
            self.db.setPassword('0000')

            self.db.open()

            print('Соединение успешно')
        except PyQt5.QtSql.QSqlError as e:
            print('Не удалось подлючиться ', e)