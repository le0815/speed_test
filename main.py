import math
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets, QtMultimediaWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import pyqtSignal, QThread

import matplotlib

# matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

from mainwindow import Ui_MainWindow
import speedtest

sp = speedtest.Speedtest(secure=True)


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('black')
        self.axes = fig.add_subplot(111)

        self.axes.set_facecolor('black')
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("QMainWindow {background: 'black';}")
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.Init()
        self.thread = {}
        self.uic.start_btn.clicked.connect(self.StarThrd)

        # line chart
        self.download_speed = 0
        self.upload_speed = 0
        self.value_list = np.array([[0, 0]])
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.df = pd.DataFrame(self.value_list)
        self.df.plot(ax=self.sc.axes, legend=False)
        self.uic.gauge_screen.addWidget(self.sc)

        # set timer to draw chart
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.Chart)


    def Chart(self):
        if self.download_speed == 0 and self.upload_speed == 0:
            return
        # Create a 1D array to add
        new_row = np.array([self.download_speed, self.upload_speed])
        self.value_list = np.vstack([self.value_list, new_row])
        print(self.value_list)
        # insert new value to chart
        self.df = pd.DataFrame(self.value_list)
        # drop label

        # remove old data
        self.sc.axes.cla()
        # draw new data
        self.df.plot(ax=self.sc.axes, legend=False)

        self.sc.draw()
        # self.sc.set_axis_off()

    def StarThrd(self):
        # speed test
        self.thread[1] = Thrd(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.GetInfo)
        # display value
        self.thread[2] = Thrd2(index=2)
        self.thread[2].start()
        self.thread[2].signal.connect(self.GetResult)
        # set text on 'go' label
        self.uic.label.setText('Đang lấy thông tin')
        # start draw chart
        self.timer.start()
    def GetInfo(self, result):
        # show ip and isp
        if result[1] == 1:
            info = result[0]
            self.uic.ip_label.show()
            self.uic.isp_label.show()
            self.uic.ip_label.setText(f'IP: {info["client"]["ip"]}')
            self.uic.isp_label.setText(f'ISP: {info["client"]["isp"]}')
            print(f"thrd1 sender: {self.senderSignalIndex()}")
        # update status on 'go' label
        if result[1] == 3:
            self.uic.label.setText(result[0])
        # display ping value
        if result[1] == 4:
            self.uic.ping_lcd.display(result[0])
        # display download speed real-time
        if result[1] == 5:
            self.uic.download_lcd.display(result[0])
        # display upload speed real-time
        if result[1] == 6:
            self.uic.upload_lcd.display(result[0])
            # reset value to init
            self.timer.stop()
            self.upload_speed = 0
            self.download_speed = 0
            self.value_list = np.array([[0, 0]])

    def GetResult(self, result):
        # display current download speed
        if result[2] == 2 and result[0] != 0:
            value = result[0]
            # hide 'go' label
            self.uic.label.hide()
            # display result to lcd
            self.uic.lcd_number.show()
            self.uic.speed_unit_label.show()
            self.uic.lcd_number.display(value)
            # redraw chart
            self.download_speed = value

        # display current upload speed
        if result[2] == 2 and result[1] != 0:
            value = result[1]
            # display result to lcd
            self.uic.lcd_number.display(value)
            # redraw chart
            self.upload_speed = value

    def Init(self):
        # label
        self.uic.label.setGeometry(0, 80, 856, 640)

        self.uic.label.setScaledContents(True)
        mv = QMovie('img/wave_edited.gif')
        self.uic.label.setMovie(mv)
        mv.start()
        self.uic.label.setStyleSheet("background-color: rgba(255,255,255,0);border: 0px;")
        # button
        # start_btn
        self.uic.start_btn.setGeometry(300, 280, 250, 250)
        self.uic.start_btn.setStyleSheet("background-color: rgba(255,255,255,0);border: 0px;")

        # app_tile
        self.uic.app_title.setGeometry(QtCore.QRect(350, 20, 101, 17))
        self.uic.app_title.setStyleSheet("color : '#737489'")
        # country_label
        self.uic.ip_label.setGeometry(QtCore.QRect(70, 500, 261, 31))
        self.uic.ip_label.setStyleSheet("color: 'white'")
        self.uic.ip_label.hide()
        # isp_label
        self.uic.isp_label.setGeometry(QtCore.QRect(70, 430, 261, 71))
        self.uic.isp_label.setStyleSheet("color: rgb(26, 95, 180);")
        self.uic.isp_label.hide()
        # lcd led
        self.uic.lcd_number.hide()
        # hide lcd unit
        self.uic.speed_unit_label.hide()


class Thrd(QtCore.QThread):
    signal = pyqtSignal(list)

    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def run(self):
        # reset down and upload value equal 0
        sp.upload_result = 0
        sp.download_result = 0
        # sp = speedtest.Speedtest(secure=True)
        status = ''
        # find server - 3
        print("Tìm kiếm server....")
        status = 'Tìm kiếm server....'
        result = [status, 3]
        self.signal.emit(result)
        sp.get_servers()
        # get best server - 3
        print("Chọn server tốt nhất...")
        status = 'Chọn server tốt nhất...'
        result = [status, 3]
        self.signal.emit(result)
        sp.get_best_server()
        # get ping - 4
        ping_result = sp.results.ping
        ping_result = round(ping_result, 2)
        print(f"Độ trễ: {ping_result}ms")
        result = [ping_result, 4]
        self.signal.emit(result)
        # get info - 3
        print("Lấy thông tin...")
        status = 'Lấy thông tin...'
        result = [status, 3]
        self.signal.emit(result)
        info = sp.get_config()
        result = [info, 1]
        self.signal.emit(result)
        # get download speed - 5
        print("Đo tốc độ tải xuống...")
        down_result = sp.download()
        down_result = round(down_result / 1024 / 1024, 2)
        result = [down_result, 5]
        self.signal.emit(result)
        print(f'{down_result / 1024 / 1024}')
        # get upload speed - 6
        print("Đo tốc độ tải lên...")
        up_result = sp.upload()
        up_result = round(up_result / 1024 / 1024, 2)
        result = [up_result, 6]
        self.signal.emit(result)
        print(f'{up_result / 1024 / 1024}')

    def stop(self):
        print('Stopping thread...', self.index)
        self.thread().exit()


class Thrd2(QtCore.QThread):
    signal = pyqtSignal(list)

    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def run(self):
        while True:
            # send download and upload speed in real-time
            result = [sp.download_result, sp.upload_result, 2]
            # print(f'upload real_time: {sp.upload_result}')
            self.signal.emit(result)
            time.sleep(0.05)

    def stop(self):
        print('Stopping thread...', self.index)
        self.thread().exit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
