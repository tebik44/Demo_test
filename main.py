import datetime
import sys
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, \
QDialog
from sqlalchemy import and_, update

from utils.model import Model, Users, Role

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('Windows/login_and_registr.ui', self)
        self.setWindowTitle('Вау, это вход!')
        self.setWindowIcon(QIcon('Source/icons/people_gesture_hand_man_icon_258682.ico'))

        self.label.setText('Вход')
        self.label_3.setText('')
        self.label_2.setText('Нету аккаунта?')

        self.pushButton.setText('Вход')
        self.pushButton_2.setText('Регистрация')

        self.pushButton.clicked.connect(self.log)
        self.pushButton_2.clicked.connect(self.reg_window)

    def log(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        session = Model().Session()
        if len(login) != 0 or len(password) != 0:
            query = session.query(Users.id_user, Users.last_come, Users.role_id).filter(and_(Users.login == login, Users.password == password)).first()

            if query:
                before_last_come = query[1]
                stmt = update(Users).where(Users.id_user == query[0]).values(last_come=datetime.datetime.now())
                session.execute(stmt)

                session.commit()
                self.profile = Profile(login=login, password=password, before_last_come=before_last_come, role_id=query[2])
                self.profile.show()
                self.hide()
        else:
            self.label_3.setText("* Все поля должны быть заполнены!")


    def reg_window(self):
        self.reg_start_polling = Registration()
        self.reg_start_polling.show()
        self.hide()




class Registration(QtWidgets.QMainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        uic.loadUi('Windows/login_and_registr.ui', self)
        self.setWindowTitle('Регистрация!')
        self.setWindowIcon(QIcon('Source/icons/people_gesture_hand_man_icon_258682.ico'))

        self.label.setText('Регистрация')
        self.label_3.setText('')
        self.label_2.setText('Есть аккаунт?')

        self.pushButton.setText('Регистрация')
        self.pushButton_2.setText('Войти')

        self.pushButton.clicked.connect(self.start_reg)
        self.pushButton_2.clicked.connect(self.log_window)


    def start_reg(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        session = Model().Session()
        query = session.query(Users.id_user).filter(and_(Users.login == login, Users.password == password)).first()

        if len(login) != 0 or len(password) != 0:
            if query is None:
                user = Users(
                    login = login,
                    password = password,
                    last_come = datetime.datetime.now(),
                    role_id = 2
                )
                try:
                    session.add(user)
                    session.commit()
                    self.label_3.setText('ВЫ УСПЕШНО ЗАРЕГИСТРИРОВАНЫ!')
                    self.label.setText('ВЫ УСПЕШНО ЗАРЕГИСТРИРОВАНЫ!')
                    time.sleep(1.7)
                    self.log_window()

                except Exception as e:
                    self.label_3.setText('Ошибка вставки данных в бд')
            else:
                self.label.setText('Такой пользователь уже создан')
        else:
            self.label_3.setText("* Все поля должны быть заполнены!")

    def log_window(self):
        self.log_start_polling = Login()
        self.log_start_polling.show()
        self.hide()






class Profile(QMainWindow):
    def __init__(self, **kwargs):
        super(Profile, self).__init__()
        uic.loadUi('Windows/login_and_registr.ui', self)
        self.setWindowTitle('Профиль!')
        self.setWindowIcon(QIcon('Source/icons/people_gesture_hand_man_icon_258682.ico'))


        self.label.setText('Профиль')
        time_of_day = {
            (4, 0): "Доброе утро",
            (12, 0): "Добрый день",
            (17, 0): "Добрый вечер"
        }

        current_time = datetime.datetime.now().time()
        greeting = next((g for time, g in time_of_day.items() if current_time < datetime.time(*time)), "Доброй ночи")

        self.label_3.setText(f"{greeting} {kwargs['login']}\n Ваш пароль: {kwargs['password']}\n "
                             f"Ваш предыдущий последний вход был {kwargs['before_last_come']}")
        self.label_2.hide()

        self.lineEdit.hide()
        self.lineEdit_2.hide()

        self.pushButton.hide()
        self.pushButton_2.hide()

        if kwargs['role_id'] == 1:
            self.tableWidget = QtWidgets.QTableWidget()
            self.tableWidget.setGeometry(50, 160, 300, 100)

            self.setCentralWidget(self.tableWidget)
            self.loaddata()
            self.setMinimumSize(1000, 1000)
    def loaddata(self):
        session = Model().Session()
        users = session.query(Users).all()

        if users:
            column_names = ['id_user', 'login', 'password', 'last_come', 'role_id']
            num_rows = len(users)
            num_columns = len(column_names)

            self.tableWidget.setRowCount(num_rows)
            self.tableWidget.setColumnCount(num_columns)

            for row_index, user in enumerate(users):
                for col_index, column_name in enumerate(column_names):
                    cell_data = getattr(user, column_name)
                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget.setItem(row_index, col_index, item)



if __name__ == '__main__':
    # Model().create_all_table()
    app = QtWidgets.QApplication([])
    login = Login()
    login.show()

    sys.exit(app.exec_())

