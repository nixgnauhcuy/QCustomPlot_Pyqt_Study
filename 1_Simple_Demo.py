import sys, math

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from QCustomPlot_PyQt5 import QCustomPlot, QCP, QCPAxisTickerTime, QCPRange

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Simple Demo")
        self.resize(400,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        # add two new graphs and set their look:
        self.customPlot.addGraph()
        self.customPlot.graph(0).setPen(QPen(Qt.blue)) # line color blue for first graph
        self.customPlot.graph(0).setBrush(QBrush(QColor(0, 0, 255, 20))) # first graph will be filled with translucent blue

        self.customPlot.addGraph()
        self.customPlot.graph(1).setPen(QPen(Qt.red)) # line color red for second graph

        # generate some points of data (y0 for first, y1 for second graph):
        x = []
        y0 = []
        y1 = []
        for i in range(251):
            x.append(i)
            y0.append(math.exp(-i/150.0)*math.cos(i/10.0)) # exponentially decaying cosine
            y1.append(math.exp(-i/150.0)) # exponential envelope

        self.customPlot.xAxis.setTicker(QCPAxisTickerTime())
        self.customPlot.xAxis.setRange(0, 250)
        self.customPlot.yAxis.setRange(-1.1, 1.1)

        # configure right and top axis to show ticks but no labels:
        # (see QCPAxisRect::setupFullAxesBox for a quicker method to do this)
        self.customPlot.xAxis2.setVisible(True)
        self.customPlot.xAxis2.setTickLabels(False)
        self.customPlot.yAxis2.setVisible(True)
        self.customPlot.yAxis2.setTickLabels(False)

        # pass data points to graphs:
        self.customPlot.graph(0).setData(x, y0)
        self.customPlot.graph(1).setData(x, y1)

        # let the ranges scale themselves so graph 0 fits perfectly in the visible area:
        self.customPlot.graph(0).rescaleAxes()
        # same thing for graph 1, but only enlarge ranges (in case graph 1 is smaller than graph 0):
        self.customPlot.graph(1).rescaleAxes(True)
        # Note: we could have also just called customPlot->rescaleAxes(); instead
        # Allow user to drag axis ranges with mouse, zoom with mouse wheel and select graphs by clicking:
        self.customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectPlottables)

        # make left and bottom axes always transfer their ranges to right and top axes:
        self.customPlot.xAxis.rangeChanged[QCPRange].connect(self.customPlot.xAxis2.setRange)
        self.customPlot.yAxis.rangeChanged[QCPRange].connect(self.customPlot.yAxis2.setRange)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
