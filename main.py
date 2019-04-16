import sys
import gui

from PyQt5 import QtGui, QtWidgets
import check
import time

field_height = 10
field_width = 10


class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.icon_miss = QtGui.QIcon()
        self.icon_miss.addPixmap(QtGui.QPixmap("icons/miss.png"),
                                 QtGui.QIcon.Normal,
                                 QtGui.QIcon.Off)

        self.icon_wound = QtGui.QIcon()
        self.icon_wound.addPixmap(QtGui.QPixmap("icons/wound.png"),
                                 QtGui.QIcon.Normal,
                                 QtGui.QIcon.Off)

        self.icon_kill = QtGui.QIcon()
        self.icon_kill.addPixmap(QtGui.QPixmap("icons/kill.png"),
                                 QtGui.QIcon.Normal,
                                 QtGui.QIcon.Off)

        self.icon_empty = QtGui.QIcon()
        self.icon_empty.addPixmap(QtGui.QPixmap("icons/empty.png"),
                                 QtGui.QIcon.Normal,
                                 QtGui.QIcon.Off)

        self.icon_maybe = QtGui.QIcon()
        self.icon_maybe.addPixmap(QtGui.QPixmap("icons/maybe.png"),
                                 QtGui.QIcon.Normal,
                                 QtGui.QIcon.Off)

        self.sea_field_t = [[' ' for _ in range(field_width)] for _ in
                            range(field_height)]


        self.all_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.timeout = 10
        # self.cell_0_0.clicked.connect(self.buttonClicked)
        for x in range(field_height):
            for y in range(field_width):
                self.cells[x][y].clicked.connect(self.buttonClicked)

        self.button_start.clicked.connect(self.button_clicked_start)

    def button_clicked_start(self):
        self.timeout = int(self.lineEdit_timeout.text())
        self.all_ships = []
        for _ in range(self.spinBox_4.value()):
            self.all_ships.append(4)

        for _ in range(self.spinBox_3.value()):
            self.all_ships.append(3)

        for _ in range(self.spinBox_2.value()):
            self.all_ships.append(2)

        for _ in range(self.spinBox_1.value()):
            self.all_ships.append(1)

        # self.statusBar.showMessage('Просчет позиции...')
        try:
            x, y = check.start(self.sea_field_t, self.all_ships, self.timeout)
            self.statusBar.showMessage(f'Готово! Бей: {x} {y}')
            self.cells[x-1][y-1].setIcon(self.icon_maybe)
        except TypeError:
            pass

    def buttonClicked(self):
        sender = self.sender()
        x, y = int(sender.objectName()[5]), int(sender.objectName()[7])
        if self.sea_field_t[x][y] == ' ':
            self.sea_field_t[x][y] = '.'
            self.cells[x][y].setIcon(self.icon_miss)
        elif self.sea_field_t[x][y] == '.':
            self.sea_field_t[x][y] = '/'
            self.cells[x][y].setIcon(self.icon_wound)
        elif self.sea_field_t[x][y] == '/':
            self.sea_field_t[x][y] = 'x'
            self.cells[x][y].setIcon(self.icon_kill)
        else:
            self.sea_field_t[x][y] = ' '
            self.cells[x][y].setIcon(self.icon_empty)

        self.statusBar.showMessage(sender.objectName() + ' was pressed')
        # print(*self.sea_field_t, sep='\n')


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

# self.cells = [[0 for _ in range(10)] for x in range(10)]
# for x in range(10):
#     for y in range(10):
#         self.cells[x][y] = QtWidgets.QPushButton(self.centralwidget)
#         self.cells[x][y].setGeometry(
#             QtCore.QRect(40 + y * 30, 40 + x * 30, 30, 30))
#         self.cells[x][y].setText("")
#         self.cells[x][y].setObjectName(f"cell_{x}_{y}")
