import sys, math, random

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor, QFont, QBrush
from PyQt5.QtCore import Qt, QLocale
from QCustomPlot_PyQt5 import QCustomPlot, QCPGraph, QCPScatterStyle, QCPTextElement, QCPAxisTickerPi, QCPErrorBars

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Multiple Axes Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom)) # period as decimal separator and comma as thousand separator
        self.customPlot.legend.setVisible(True)

        legendFont = self.font()  # start out with MainWindow's font..
        legendFont.setPointSize(9) # and make a bit smaller for legend
        self.customPlot.legend.setFont(legendFont)
        self.customPlot.legend.setBrush(QBrush(QColor(255,255,255,230)))
        # by default, the legend is in the inset layout of the main axis rect. So this is how we access it to change legend placement:
        self.customPlot.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignBottom|Qt.AlignRight)

        # setup for graph 0: key axis left, value axis bottom
        # will contain left maxwell-like function
        self.customPlot.addGraph(self.customPlot.yAxis, self.customPlot.xAxis)
        self.customPlot.graph(0).setPen(QPen(QColor(255, 100, 0)))
        self.customPlot.graph(0).setLineStyle(QCPGraph.lsLine)
        self.customPlot.graph(0).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssDisc, 5))
        self.customPlot.graph(0).setName("Left maxwell function")

        # setup for graph 1: key axis bottom, value axis left (those are the default axes)
        # will contain bottom maxwell-like function with error bars
        self.customPlot.addGraph()
        self.customPlot.graph(1).setPen(QPen(Qt.red))
        self.customPlot.graph(1).setLineStyle(QCPGraph.lsStepCenter)
        self.customPlot.graph(1).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, Qt.red, Qt.white, 7))
        self.customPlot.graph(1).setName("Bottom maxwell function")
        errorBars = QCPErrorBars(self.customPlot.xAxis, self.customPlot.yAxis)
        errorBars.removeFromLegend()
        errorBars.setDataPlottable(self.customPlot.graph(1))

        # setup for graph 2: key axis top, value axis right
        # will contain high frequency sine with low frequency beating:
        self.customPlot.addGraph(self.customPlot.xAxis2, self.customPlot.yAxis2)
        self.customPlot.graph(2).setPen(QPen(Qt.blue))
        self.customPlot.graph(2).setName("High frequency sine")

        # setup for graph 3: same axes as graph 2
        # will contain low frequency beating envelope of graph 2
        self.customPlot.addGraph(self.customPlot.xAxis2, self.customPlot.yAxis2)
        blueDotPen = QPen(QColor(30, 40, 255, 150))
        blueDotPen.setStyle(Qt.DotLine)
        blueDotPen.setWidthF(4)
        self.customPlot.graph(3).setPen(blueDotPen)
        self.customPlot.graph(3).setName("Sine envelope")

        # setup for graph 4: key axis right, value axis top
        # will contain parabolically distributed data points with some random perturbance
        self.customPlot.addGraph(self.customPlot.yAxis2, self.customPlot.xAxis2)
        self.customPlot.graph(4).setPen(QPen(QColor(50, 50, 50, 255)))
        self.customPlot.graph(4).setLineStyle(QCPGraph.lsNone)
        self.customPlot.graph(4).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, 4))
        self.customPlot.graph(4).setName("Some random data around\na quadratic function")

        # generate data, just playing with numbers, not much to learn here:
        x0 = [3*i/25.0 for i in range(25)]
        y0 = [math.exp(-x*x*0.8)*(x*x+x) for x in x0]
        self.customPlot.graph(0).setData(x0, y0)

        x1 = [3*i/15.0 for i in range(15)]
        y1 = [math.exp(-x*x)*(x*x)*2.6 for x in x1]
        y1err = [y*0.25 for y in y1]
        self.customPlot.graph(1).setData(x1, y1)
        errorBars.setData(y1err, y1err)

        x2 = [i/250.0*3*math.pi for i in range(250)]
        y2 = [math.sin(x*12)*math.cos(x)*10 for x in x2]
        self.customPlot.graph(2).setData(x2, y2)

        x3 = x2
        y3 = [math.cos(x)*10 for x in x3]
        self.customPlot.graph(3).setData(x3, y3)

        x4 = [i/250.0*100-50 for i in range(250)]
        y4 = [0.01*x*x + 1.5*(random.random()-0.5) + 1.5*math.pi for x in x4]
        self.customPlot.graph(4).setData(x4, y4)

        # activate top and right axes, which are invisible by default:
        self.customPlot.xAxis2.setVisible(True)
        self.customPlot.yAxis2.setVisible(True)

        # set ranges appropriate to show data:
        self.customPlot.xAxis.setRange(0, 2.7)
        self.customPlot.yAxis.setRange(0, 2.6)
        self.customPlot.xAxis2.setRange(0, 3.0*math.pi)
        self.customPlot.yAxis2.setRange(-70, 35)

        # set pi ticks on top axis:
        self.customPlot.xAxis2.setTicker(QCPAxisTickerPi())

        # add title layout element:
        self.customPlot.plotLayout().insertRow(0)
        self.customPlot.plotLayout().addElement(0, 0, QCPTextElement(self.customPlot, "Way too many graphs in one plot", QFont("sans", 12, QFont.Bold)))

        # set labels:
        self.customPlot.xAxis.setLabel("Bottom axis with outward ticks")
        self.customPlot.yAxis.setLabel("Left axis label")
        self.customPlot.xAxis2.setLabel("Top axis label")
        self.customPlot.yAxis2.setLabel("Right axis label")

        # make ticks on bottom axis go outward:
        self.customPlot.xAxis.setTickLength(0, 5)
        self.customPlot.xAxis.setSubTickLength(0, 3)

        # make ticks on right axis go inward and outward:
        self.customPlot.yAxis2.setTickLength(3, 3)
        self.customPlot.yAxis2.setSubTickLength(1, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
