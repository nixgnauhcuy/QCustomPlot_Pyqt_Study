import sys, math, random

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor, QFont, QBrush, QLinearGradient
from PyQt5.QtCore import Qt
from QCustomPlot_PyQt5 import QCustomPlot, QCPGraph, QCPScatterStyle, QCPBars, QCPLineEnding

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Styled Plot Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        # prepare data:
        x1 = [i/(20-1)*10 for i in range(20)]
        y1 = [math.cos(x*0.8+math.sin(x*0.16+1.0))*math.sin(x*0.54)+1.4 for x in x1]
        x2 = [i/(100-1)*10 for i in range(100)]
        y2 = [math.cos(x*0.85+math.sin(x*0.165+1.1))*math.sin(x*0.50)+1.7 for x in x2]
        x3 = [i/(20-1)*10 for i in range(20)]
        y3 = [0.05+3*(0.5+math.cos(x*x*0.2+2)*0.5)/(x+0.7)+random.random()/100 for x in x3]
        x4 = x3
        y4 = [(0.5-y)+((x-2)*(x-2)*0.02) for x,y in zip(x4,y3)]

        # create and configure plottables:
        graph1 = QCPGraph(self.customPlot.xAxis, self.customPlot.yAxis)
        graph1.setData(x1, y1)
        graph1.setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, QPen(Qt.black, 1.5), QBrush(Qt.white), 9))
        graph1.setPen(QPen(QColor(120, 120, 120), 2))

        graph2 = QCPGraph(self.customPlot.xAxis, self.customPlot.yAxis)
        graph2.setData(x2, y2)
        graph2.setPen(QPen(Qt.PenStyle.NoPen))
        graph2.setBrush(QColor(200, 200, 200, 20))
        graph2.setChannelFillGraph(graph1)

        bars1 = QCPBars(self.customPlot.xAxis, self.customPlot.yAxis)
        bars1.setWidth(9/(20-1))
        bars1.setData(x3, y3)
        bars1.setPen(QPen(Qt.PenStyle.NoPen))
        bars1.setBrush(QColor(10, 140, 70, 160))

        bars2 = QCPBars(self.customPlot.xAxis, self.customPlot.yAxis)
        bars2.setWidth(9/(20-1))
        bars2.setData(x4, y4)
        bars2.setPen(QPen(Qt.PenStyle.NoPen))
        bars2.setBrush(QColor(10, 100, 50, 70))
        bars2.moveAbove(bars1)

        # move bars above graphs and grid below bars:
        self.customPlot.addLayer("abovemain", self.customPlot.layer("main"), QCustomPlot.limAbove)
        self.customPlot.addLayer("belowmain", self.customPlot.layer("main"), QCustomPlot.limBelow)
        graph1.setLayer("abovemain")
        self.customPlot.xAxis.grid().setLayer("belowmain")
        self.customPlot.yAxis.grid().setLayer("belowmain")

        # set some pens, brushes and backgrounds:
        self.customPlot.xAxis.setBasePen(QPen(Qt.white, 1))
        self.customPlot.yAxis.setBasePen(QPen(Qt.white, 1))
        self.customPlot.xAxis.setTickPen(QPen(Qt.white, 1))
        self.customPlot.yAxis.setTickPen(QPen(Qt.white, 1))
        self.customPlot.xAxis.setSubTickPen(QPen(Qt.white, 1))
        self.customPlot.yAxis.setSubTickPen(QPen(Qt.white, 1))
        self.customPlot.xAxis.setTickLabelColor(Qt.white)
        self.customPlot.yAxis.setTickLabelColor(Qt.white)
        self.customPlot.xAxis.grid().setPen(QPen(QColor(140, 140, 140), 1, Qt.DotLine))
        self.customPlot.yAxis.grid().setPen(QPen(QColor(140, 140, 140), 1, Qt.DotLine))
        self.customPlot.xAxis.grid().setSubGridPen(QPen(QColor(80, 80, 80), 1, Qt.DotLine))
        self.customPlot.yAxis.grid().setSubGridPen(QPen(QColor(80, 80, 80), 1, Qt.DotLine))
        self.customPlot.xAxis.grid().setSubGridVisible(True)
        self.customPlot.yAxis.grid().setSubGridVisible(True)
        self.customPlot.xAxis.grid().setZeroLinePen(QPen(Qt.PenStyle.NoPen))
        self.customPlot.yAxis.grid().setZeroLinePen(QPen(Qt.PenStyle.NoPen))
        self.customPlot.xAxis.setUpperEnding(QCPLineEnding(QCPLineEnding.esSpikeArrow))
        self.customPlot.yAxis.setUpperEnding(QCPLineEnding(QCPLineEnding.esSpikeArrow))

        plotGradient = QLinearGradient()
        plotGradient.setStart(0, 0)
        plotGradient.setFinalStop(0, 350)
        plotGradient.setColorAt(0, QColor(80, 80, 80))
        plotGradient.setColorAt(1, QColor(50, 50, 50))
        self.customPlot.setBackground(plotGradient)
        axisRectGradient = QLinearGradient()
        axisRectGradient.setStart(0, 0)
        axisRectGradient.setFinalStop(0, 350)
        axisRectGradient.setColorAt(0, QColor(80, 80, 80))
        axisRectGradient.setColorAt(1, QColor(30, 30, 30))
        self.customPlot.axisRect().setBackground(axisRectGradient)
        self.customPlot.rescaleAxes()
        self.customPlot.yAxis.setRange(0, 2)
        self.customPlot.legend.setVisible(True)
        self.customPlot.legend.setFont(QFont("Helvetica", 9))
        self.customPlot.legend.setRowSpacing(-3)
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
