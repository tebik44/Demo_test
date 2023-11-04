import datetime
import sys
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, \
    QDialog, QMessageBox, QLineEdit
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

        self.pushButton.setAutoDefault(True)
        self.pushButton.setDefault(True)
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
                if query[2] == 1:
                    self.admin_panel = AdminProfile(login=login, password=password, before_last_come=before_last_come, role_id=query[2])
                    self.admin_panel.show()
                    self.hide()
                else:
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
                    # self.label_3.setText('ВЫ УСПЕШНО ЗАРЕГИСТРИРОВАНЫ!')
                    # self.label.setText('ВЫ УСПЕШНО ЗАРЕГИСТРИРОВАНЫ!')
                    message_box = QMessageBox()
                    message_box.setWindowTitle("Регистрация")
                    message_box.setText("Успешно создан аккаунт")
                    message_box.setIcon(QMessageBox.Information)
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
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
            (4, 12): "Доброе утро",
            (13, 17): "Добрый день",
            (17, 24): "Добрый вечер"
        }

        current_time = datetime.datetime.now().time().hour
        greeting = next((g for time, g in time_of_day.items() if time[0] <= current_time <= time[1]), "Доброй ночи")

        # for time, text in time_of_day.items():
        #     if time[0] <= current_time <= time[1]:
        #         greeting = text

        self.label_3.setText(f"{greeting} {kwargs['login']}\n Ваш пароль: {kwargs['password']}\n "
                             f"Ваш предыдущий последний вход был {kwargs['before_last_come']}")
        self.label_2.hide()

        self.lineEdit.hide()
        self.lineEdit_2.hide()

        self.pushButton.setText('Выход')
        self.pushButton.clicked.connect(self.exit)
        self.pushButton_2.hide()

    def exit(self):
        self.log_start_polling = Login()
        self.log_start_polling.show()
        self.hide()


class AdminProfile(QMainWindow):
    def __init__(self, **kwargs):
        super(AdminProfile, self).__init__()
        uic.loadUi('Windows/admin_panel.ui', self)

        # self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        # self.pushButton = self.findChild(QPushButton, "pushButton")
        # self.tableWidget = self.findChild(QTableWidget, 'tableWidget')
        #
        # layout = QVBoxLayout()
        #
        # layout.addWidget(self.lineEdit)
        # layout.addWidget(self.pushButton)
        # layout.addWidget(self.tableWidget)
        #
        # central_widget = QWidget()
        # central_widget.setLayout(layout)
        # self.setCentralWidget(central_widget)

        self.sort_order = Qt.AscendingOrder
        self.lineEdit.setPlaceholderText('Поиск по логину')
        self.pushButton.clicked.connect(self.filter_user)
        # self.setCentralWidget(self.tableWidget)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setSortIndicator(0, Qt.DescendingOrder)
        self.tableWidget.setSortingEnabled(True)

        self.tableWidget.horizontalHeader().sectionClicked.connect(self.sort_table)
        session = Model().Session()
        self.loaddata(session.query(Users).all())
        session.close()
        self.item_change_in_progress = False

        self.tableWidget.itemChanged.connect(self.handle_item_changed)

        self.setMinimumSize(1000, 1000)
        self.setMaximumSize(1000, 1000)


    def button_item_changed(self):
        self.tableWidget.itemChanged.connect(self.handle_item_changed)

    def handle_item_changed(self, item):
        id_item = self.tableWidget.item(item.row(), item.column())
        self.tableWidget.itemChanged.disconnect(self.handle_item_changed)
        if not self.item_change_in_progress:
            self.item_change_in_progress = True
            if id_item:
                change_data = item.text()
                session = Model().Session()
                column_name = self.tableWidget.horizontalHeaderItem(item.column())
                id_field = self.tableWidget.item(item.row(), 0)
                id_field = id_field.text()
                query = update(Users).where(Users.id_user==id_field).values({column_name.text(): change_data})
                session.execute(query)
                session.commit()
                # self.tableWidget.itemChanged.connect(self.handle_item_changed)
                self.item_change_in_progress = False
                self.tableWidget.itemChanged.connect(self.handle_item_changed)
                self.loaddata(session.query(Users).all())
                # query = Users.update().value(column_name=item.text()).where(Users.id_user=id_item)


    def filter_user(self):
        filter_text = self.lineEdit.text()
        session = Model().Session()
        if filter_text:
            query = session.query(Users).filter(Users.login == filter_text).all()
            self.loaddata(query)
        else:
            self.loaddata(session.query(Users).all())

    def sort_table(self, index):
        # if self.sort_order == Qt.AscendingOrder:
        #     new_order = Qt.DescendingOrder
        # else:
        #     new_order = Qt.AscendingOrder
        self.tableWidget.sortItems(index, Qt.AscendingOrder)

    def loaddata(self, data):
        if data:
            column_names = ['id_user', 'login', 'password', 'last_come', 'role_id']
            num_rows = len(data)
            num_columns = len(column_names)

            self.tableWidget.setRowCount(num_rows)
            self.tableWidget.setColumnCount(num_columns)
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            # self.tableWidget.setMaximumSize(500, 500)

            for row_index, user in enumerate(data):
                for col_index, column_name in enumerate(column_names):
                    cell_data = getattr(user, column_name)
                    item = QTableWidgetItem(str(cell_data))
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    self.tableWidget.setItem(row_index, col_index, item)
            # self.tableWidget.itemChanged.connect(self.handle_item_changed)


if __name__ == '__main__':
    # Model().create_all_table()
    app = QtWidgets.QApplication([])
    login = Login()
    login.show()

    sys.exit(app.exec_())

