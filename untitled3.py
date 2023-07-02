# coding: utf-8
import sys
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Window size
        self.WIDTH = 300
        self.HEIGHT = 300
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_menu)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.6)

        radius = 150
        self.centralwidget.setStyleSheet(
            """
            background:rgb(255, 255, 255);
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )

    def right_menu(self, pos):
        menu = QMenu()

        # Add menu options
        exit_option = menu.addAction('Exit')

        # Menu option events
        exit_option.triggered.connect(lambda: exit())

        # Position
        menu.exec_(self.mapToGlobal(pos))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.moveFlag = False
        self.setCursor(Qt.CrossCursor)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())