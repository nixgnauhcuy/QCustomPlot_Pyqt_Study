import sys, math, random

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt, QTime, QTimer

from QCustomPlot_PyQt5 import QCustomPlot, QCPAxisTickerTime

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Realtime Data Demo")
        self.resize(600,400)

        self.lastPointKey = 0

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.addGraph()
        self.customPlot.graph(0).setPen(QPen(QColor(40, 110, 255)))
        self.customPlot.addGraph()
        self.customPlot.graph(1).setPen(QPen(QColor(255, 110, 40)))

        timeTicker = QCPAxisTickerTime()
        timeTicker.setTimeFormat("%h:%m:%s")
        self.customPlot.xAxis.setTicker(timeTicker)
        self.customPlot.axisRect().setupFullAxesBox()
        self.customPlot.yAxis.setRange(-1.2, 1.2)

        # make left and bottom axes transfer their ranges to right and top axes:
        self.customPlot.xAxis.rangeChanged.connect(self.customPlot.xAxis2.setRange)
        self.customPlot.yAxis.rangeChanged.connect(self.customPlot.yAxis2.setRange)

        # setup a timer that repeatedly calls MainWindow::realtimeDataSlot:
        self.curTime = QTime.currentTime()
        self.dataTimer = QTimer(self)
        self.dataTimer.timeout.connect(self.realtimeDataSlot)
        self.dataTimer.start(0) # Interval 0 means to refresh as fast as possible

    def realtimeDataSlot(self) -> None:
        # calculate two new data points:
        key = self.curTime.msecsTo(QTime.currentTime())/1000.0
        
        if key-self.lastPointKey > 0.002: # at most add point every 2 ms
            # add data to lines:
            self.customPlot.graph(0).addData(key, math.sin(key)+random.random()*1*math.sin(key/0.3843))
            self.customPlot.graph(1).addData(key, math.cos(key)+random.random()*0.5*math.sin(key/0.4364))
            # rescale value (vertical) axis to fit the current data:
            # self.customPlot.graph(0).rescaleValueAxis()
            # self.customPlot.graph(1).rescaleValueAxis(True)
            self.lastPointKey = key

        # make key axis range scroll with the data (at a constant range size of 8):
        self.customPlot.xAxis.setRange(key, 8, Qt.AlignRight)
        self.customPlot.replot()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
