import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QMessageBox
from PyQt5 import QtCore, QtWidgets
import sqlite3
from mainUI import Ui_MainWindow
from addEditCoffeeFormUI import Ui_Form
import os

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

con = sqlite3.connect(os.getcwd() + '\data\coffee.sqlite')
cur = con.cursor()

PARAMETERS = ['ID', 'Название_сорта', 'Степень_обжарки', 'Молотый_или_в_зернах', 'Описание_вкуса', 'Цена',
              'Объем_упаковки']


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Почти правдивая информация про кофе')
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.Stat_for_table)
        self.pushButton_2.clicked.connect(self.Database_change)

        name = cur.execute("""SELECT DISTINCT Название_сорта from coffee""").fetchall()
        name = [str(*i) for i in name]

        self.comboBox.addItems(name)

    def Stat_for_table(self):
        coffee = self.comboBox.currentText()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setVerticalHeaderLabels(['Кофе'])
        self.tableWidget.setHorizontalHeaderLabels(PARAMETERS)
        for t, i in enumerate(PARAMETERS):
            p = str(*cur.execute(f"""SELECT DISTINCT {PARAMETERS[t]} from coffee
                 where Название_сорта = '{coffee}'""").fetchall()[0])
            self.tableWidget.setItem(0, t, QTableWidgetItem(p))

    def Database_change(self):
        self.form2 = Form2()
        self.form2.show()
        self.close()


class Form2(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.f = False
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setVerticalHeaderLabels(['Кофе'])
        self.tableWidget.setHorizontalHeaderLabels(PARAMETERS[1:])

        self.pushButton.clicked.connect(self.upd)
        self.pushButton_2.clicked.connect(self.Search)
        self.pushButton_3.clicked.connect(self.ret)

    def Search(self):
        self.coffee_id = self.lineEdit.text()
        if self.coffee_id == '':
            error = Dialog('Ошибка!', 'Вы не выбрали id кофе, которого хотите изменить!', QMessageBox.Warning)
            error.messbox()
        else:
            self.f = True
            self.q = cur.execute(f"""SELECT DISTINCT Название_сорта from coffee
                 where ID = '{self.coffee_id}'""").fetchall()
            if len(self.q):
                for t in range(1, len(PARAMETERS)):
                    p = str(*cur.execute(f"""SELECT DISTINCT {PARAMETERS[t]} from coffee
                                where ID = '{self.coffee_id}'""").fetchall()[0])
                    self.tableWidget.setItem(0, t - 1, QTableWidgetItem(p))
            else:
                self.lineEdit.setText('')
                error = Dialog('Ошибка!', 'Убедитесь в правильности ID кофе!', QMessageBox.Warning)
                error.messbox()

    def upd(self):
        if self.f:
            self.zxc = []
            self.zxc.append(self.coffee_id)
            for i in range(6):
                self.zxc.append(self.tableWidget.item(0, i).text())
            if len(self.q):
                for i, t in zip(PARAMETERS, self.zxc):
                    cur.execute(f"""update coffee SET {i} = '{t}' WHERE ID = '{self.coffee_id}' """).fetchall()
                con.commit()
                dio = Dialog('Успешно!', 'Вы успешно обновили БД!', QMessageBox.Information)
                dio.messbox()
        else:
            error = Dialog('Ошибка!', 'Вы не выбрали id кофе, которого хотите изменить, или выбрали некорректное ID!',
                           QMessageBox.Warning)
            error.messbox()

    def ret(self):
        self.form1 = MyWidget()
        self.form1.show()
        self.close()


class Dialog:
    def __init__(self, title, mess, icon):
        self.title = title
        self.mess = mess
        self.icon = icon

    def messbox(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.title)
        msg.setText(self.mess)
        msg.setIcon(self.icon)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
