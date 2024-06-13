import sys, math, random

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QLocale
from QCustomPlot_PyQt5 import QCustomPlot, QCPGraph, QCPScatterStyle, QCPErrorBars

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Sinc Scatter Demo")
        self.resize(400,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.legend.setVisible(True)
        self.customPlot.legend.setFont(QFont("Helvetica",9))
        # set locale to english, so we get english decimal separator:
        self.customPlot.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        # add confidence band graphs:
        self.customPlot.addGraph()
        self.pen = QPen(Qt.PenStyle.DotLine)
        self.pen.setWidth(1)
        self.pen.setColor(QColor(180,180,180))
        self.customPlot.graph(0).setName("Confidence Band 68%")
        self.customPlot.graph(0).setPen(self.pen)
        self.customPlot.graph(0).setBrush(QBrush(QColor(255,50,30,20)))
        self.customPlot.addGraph()
        self.customPlot.legend.removeItem(self.customPlot.legend.itemCount()-1) # don't show two confidence band graphs in legend
        self.customPlot.graph(1).setPen(self.pen)
        self.customPlot.graph(0).setChannelFillGraph(self.customPlot.graph(1))
        
        # add theory curve graph:
        self.customPlot.addGraph()
        self.pen.setStyle(Qt.PenStyle.DashLine)
        self.pen.setWidth(2)
        self.pen.setColor(Qt.GlobalColor.red)
        self.customPlot.graph(2).setPen(self.pen)
        self.customPlot.graph(2).setName("Theory Curve")
        # add data point graph:
        self.customPlot.addGraph()
        self.customPlot.graph(3).setPen(QPen(Qt.GlobalColor.blue))
        self.customPlot.graph(3).setLineStyle(QCPGraph.lsNone)
        self.customPlot.graph(3).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCross, 4))
        # add error bars:
        self.errorBars = QCPErrorBars(self.customPlot.xAxis, self.customPlot.yAxis)
        self.errorBars.removeFromLegend()
        self.errorBars.setAntialiased(False)
        self.errorBars.setDataPlottable(self.customPlot.graph(3))
        self.errorBars.setPen(QPen(QColor(180,180,180)))
        self.customPlot.graph(3).setName("Measurement")
        
        # generate ideal sinc curve data and some randomly perturbed data for scatter plot:
        x0 = []
        y0 = []
        yConfUpper = []
        yConfLower = []
        for i in range(250):
            x0.append((i/249.0-0.5)*30+0.01) # by adding a small offset we make sure not do divide by zero in next code line
            y0.append(math.sin(x0[i])/x0[i]) # sinc function
            yConfUpper.append(y0[i]+0.15)
            yConfLower.append(y0[i]-0.15)
            x0[i] *= 1000
        x1 = []
        y1 = []
        y1err = []
        for i in range(50):
            # generate a gaussian distributed random number:
            tmp1 = random.random()
            tmp2 = random.random()
            r = math.sqrt(-2*math.log(tmp1))*math.cos(2*math.pi*tmp2) # box-muller transform for gaussian distribution
            # set y1 to value of y0 plus a random gaussian pertubation:
            x1.append((i/50.0-0.5)*30+0.25)
            y1.append(math.sin(x1[i])/x1[i]+r*0.15)
            x1[i] *= 1000
            y1err.append(0.15)
        # pass data to graphs and let QCustomPlot determine the axes ranges so the whole thing is visible:
        self.customPlot.graph(0).setData(x0, yConfUpper)
        self.customPlot.graph(1).setData(x0, yConfLower)
        self.customPlot.graph(2).setData(x0, y0)
        self.customPlot.graph(3).setData(x1, y1)
        self.errorBars.setData(y1err, y1err) # Wanging: There may be something wrong here
        self.customPlot.graph(2).rescaleAxes()
        self.customPlot.graph(3).rescaleAxes(True)
        # setup look of bottom tick labels:
        self.customPlot.xAxis.setTickLabelRotation(30)
        self.customPlot.xAxis.ticker().setTickCount(9)
        self.customPlot.xAxis.setNumberFormat("ebc")
        self.customPlot.xAxis.setNumberPrecision(1)
        self.customPlot.xAxis.moveRange(-10)
        # make top right axes clones of bottom left axes. Looks prettier:
        self.customPlot.axisRect().setupFullAxesBox()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
