import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtCore
import time
from gui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.thread = {}

        self.uic.Button_start_1.clicked.connect(self.start_worker_1)
        self.uic.Button_start_2.clicked.connect(self.start_worker_2)

        self.uic.Button_stop_1.clicked.connect(self.stop_worker_1)
        self.uic.Button_stop_2.clicked.connect(self.stop_worker_2)

    def start_worker_1(self):
        self.thread[1] = ThreadClass(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.my_function)
        self.uic.Button_start_1.setEnabled(False)
        self.uic.Button_stop_1.setEnabled(True)

    def start_worker_2(self):
        self.thread[2] = ThreadClass_1(index=2)
        self.thread[2].start()
        self.thread[2].signal_1.connect(self.new_funtion)
        self.uic.Button_start_2.setEnabled(False)
        self.uic.Button_stop_2.setEnabled(True)

    def stop_worker_1(self):
        self.thread[1].stop()
        self.uic.lcdNumber_1.display(0)
        self.uic.Button_stop_1.setEnabled(False)
        self.uic.Button_start_1.setEnabled(True)

    def stop_worker_2(self):
        self.thread[2].stop()
        self.uic.lcdNumber_2.display(0)
        self.uic.Button_stop_2.setEnabled(False)
        self.uic.Button_start_2.setEnabled(True)

    def my_function(self, counter):
        m = counter
        if m == 1:
            self.uic.lcdNumber_1.display(1)
        elif m == 3:
            self.uic.lcdNumber_1.display(2)
        elif m == 6:
            self.uic.lcdNumber_1.display(3)
        elif m == 10:
            self.uic.lcdNumber_1.display(4)

    def new_funtion(self, counter_1):
        m = counter_1
        self.uic.lcdNumber_2.display(m)


class ThreadClass(QtCore.QThread):
    signal = pyqtSignal(int)

    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def run(self):
        print('Starting thread...', self.index)
        counter = 0
        while True:
            counter += 1
            self.signal.emit(counter)
            print(counter)
            time.sleep(1)
            if counter == 10:
                counter = 0

    def stop(self):
        print('Stopping thread...', self.index)
        self.terminate()


class ThreadClass_1(QtCore.QThread):
    signal_1 = pyqtSignal(int)

    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def run(self):
        print('Starting thread...', self.index)
        counter_1 = 0
        while True:
            counter_1 += 1
            self.signal_1.emit(counter_1)
            print(counter_1)
            time.sleep(0.1)
            if counter_1 == 100:
                counter_1 = 0

    def stop(self):
        print('Stopping thread...', self.index)
        self.terminate()


if _name_ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
