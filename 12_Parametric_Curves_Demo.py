import sys, math

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor, QBrush, QRadialGradient
from PyQt5.QtCore import QPointF
from QCustomPlot_PyQt5 import QCustomPlot, QCP, QCPCurve, QCPCurveData

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Parametric Curves Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        # create empty curve objects:
        self.fermatSpiral1 = QCPCurve(self.customPlot.xAxis, self.customPlot.yAxis)
        self.fermatSpiral2 = QCPCurve(self.customPlot.xAxis, self.customPlot.yAxis)
        self.deltoidRadial = QCPCurve(self.customPlot.xAxis, self.customPlot.yAxis)

        # generate the curve data points:
        pointCount = 500
        dataSpiral1 = [QCPCurveData() for i in range(pointCount)]
        dataSpiral2 = [QCPCurveData() for i in range(pointCount)]
        dataDeltoid = [QCPCurveData() for i in range(pointCount)]
        for i in range(pointCount):
            phi = i/(pointCount-1)*8*math.pi
            theta = i/(pointCount-1)*2*math.pi
            dataSpiral1[i] = QCPCurveData(i, math.sqrt(phi)*math.cos(phi), math.sqrt(phi)*math.sin(phi))
            dataSpiral2[i] = QCPCurveData(i, -dataSpiral1[i].key, -dataSpiral1[i].value)
            dataDeltoid[i] = QCPCurveData(i, 2*math.cos(2*theta)+math.cos(1*theta)+2*math.sin(theta), 2*math.sin(2*theta)-math.sin(1*theta))

        # pass the data to the curves; we know t (i in loop above) is ascending, so set alreadySorted=True (saves an extra internal sort):
        self.fermatSpiral1.data().set(dataSpiral1, True)
        self.fermatSpiral2.data().set(dataSpiral2, True)
        self.deltoidRadial.data().set(dataDeltoid, True)

        # color the curves:
        self.fermatSpiral1.setPen(QPen(QColor(0, 0, 255)))
        self.fermatSpiral1.setBrush(QBrush(QColor(0, 0, 255, 20)))
        self.fermatSpiral2.setPen(QPen(QColor(255, 120, 0)))
        self.fermatSpiral2.setBrush(QBrush(QColor(255, 120, 0, 30)))
        radialGrad = QRadialGradient(QPointF(310, 180), 200)
        radialGrad.setColorAt(0, QColor(170, 20, 240, 100))
        radialGrad.setColorAt(0.5, QColor(20, 10, 255, 40))
        radialGrad.setColorAt(1,QColor(120, 20, 240, 10))
        self.deltoidRadial.setPen(QPen(QColor(170, 20, 240)))
        self.deltoidRadial.setBrush(QBrush(radialGrad))

        # set some basic customPlot config:
        self.customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectPlottables)
        self.customPlot.axisRect().setupFullAxesBox()
        self.customPlot.rescaleAxes()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
