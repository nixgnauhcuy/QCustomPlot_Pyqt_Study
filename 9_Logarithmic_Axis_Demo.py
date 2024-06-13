import sys, math

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import Qt
from QCustomPlot_PyQt5 import QCustomPlot, QCPGraph, QCPGraphData, QCP, QCPAxis, QCPAxisTickerLog

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Logarithmic Axis Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.setNoAntialiasingOnDrag(True) # more performance/responsiveness during dragging
        self.customPlot.addGraph()
        pen = QPen(QColor(255,170,100))
        pen.setWidth(2)
        pen.setStyle(Qt.DotLine)
        self.customPlot.graph(0).setPen(pen)
        self.customPlot.graph(0).setName("x")

        self.customPlot.addGraph()
        self.customPlot.graph(1).setPen(QPen(Qt.red))
        self.customPlot.graph(1).setBrush(QBrush(QColor(255, 0, 0, 20)))
        self.customPlot.graph(1).setName("-sin(x)exp(x)")

        self.customPlot.addGraph()
        self.customPlot.graph(2).setPen(QPen(Qt.blue))
        self.customPlot.graph(2).setBrush(QBrush(QColor(0, 0, 255, 20)))
        self.customPlot.graph(2).setName(" sin(x)exp(x)")

        self.customPlot.addGraph()
        pen = QPen(QColor(0,0,0))
        pen.setWidth(1)
        pen.setStyle(Qt.DashLine)
        self.customPlot.graph(3).setPen(pen)
        self.customPlot.graph(3).setBrush(QBrush(QColor(0,0,0,15)))
        self.customPlot.graph(3).setLineStyle(QCPGraph.lsStepCenter)
        self.customPlot.graph(3).setName("x!")

        dataCount = 200
        dataFactorialCount = 21
        dataLinear = [QCPGraphData() for i in range(dataCount)]
        dataMinusSinExp = [QCPGraphData() for i in range(dataCount)]
        dataPlusSinExp = [QCPGraphData() for i in range(dataCount)]
        dataFactorial = [QCPGraphData() for i in range(dataFactorialCount)]
        for i in range(dataCount):
            dataLinear[i].key = i/10.0
            dataLinear[i].value = dataLinear[i].key
            dataMinusSinExp[i].key = i/10.0
            dataMinusSinExp[i].value = -math.sin(dataMinusSinExp[i].key)*math.exp(dataMinusSinExp[i].key)
            dataPlusSinExp[i].key = i/10.0
            dataPlusSinExp[i].value = math.sin(dataPlusSinExp[i].key)*math.exp(dataPlusSinExp[i].key)
        for i in range(dataFactorialCount):
            dataFactorial[i].key = i
            dataFactorial[i].value = 1.0
            for k in range(1, i+1):
                dataFactorial[i].value *= k

        self.customPlot.graph(0).data().set(dataLinear)
        self.customPlot.graph(1).data().set(dataMinusSinExp)
        self.customPlot.graph(2).data().set(dataPlusSinExp)
        self.customPlot.graph(3).data().set(dataFactorial)
        
        self.customPlot.xAxis.grid().setSubGridVisible(True)
        self.customPlot.yAxis.grid().setSubGridVisible(True)
        self.customPlot.yAxis.setScaleType(QCPAxis.stLogarithmic)
        self.customPlot.yAxis2.setScaleType(QCPAxis.stLogarithmic)
        logTicker = QCPAxisTickerLog()
        self.customPlot.yAxis.setTicker(logTicker)
        self.customPlot.yAxis2.setTicker(logTicker)
        self.customPlot.yAxis.setNumberFormat("eb") # e = exponential, b = beautiful decimal powers
        self.customPlot.yAxis.setNumberPrecision(0) # makes sure "1*10^4" is displayed only as "10^4"
        self.customPlot.xAxis.setRange(0, 19.9)
        self.customPlot.yAxis.setRange(1e-2, 1e10)
        # make range draggable and zoomable:
        self.customPlot.setInteractions(QCP.Interactions(QCP.iRangeDrag | QCP.iRangeZoom))
        # make top right axes clones of bottom left axes:
        self.customPlot.axisRect().setupFullAxesBox()
        # connect signals so top and right axes move in sync with bottom and left axes:
        self.customPlot.xAxis.rangeChanged.connect(self.customPlot.xAxis2.setRange)
        self.customPlot.yAxis.rangeChanged.connect(self.customPlot.yAxis2.setRange)

        self.customPlot.legend.setVisible(True)
        self.customPlot.legend.setBrush(QBrush(QColor(255,255,255,150)))
        self.customPlot.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignLeft|Qt.AlignTop) # make legend align in top left corner or axis rect

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
