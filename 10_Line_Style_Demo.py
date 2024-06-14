import sys, math

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor, QFont
from QCustomPlot_PyQt5 import QCustomPlot, QCPGraph, QCPScatterStyle

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Line Style Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.legend.setVisible(True)
        self.customPlot.legend.setFont(QFont("Helvetica", 9))
        pen = QPen()
        lineNames = ["lsNone", "lsLine", "lsStepLeft", "lsStepRight", "lsStepCenter", "lsImpulse"]
        # add graphs with different line styles:
        for i in range(QCPGraph.lsNone, QCPGraph.lsImpulse+1):
            self.customPlot.addGraph()
            pen.setColor(QColor(int(math.sin(i*1+1.2)*80+80), int(math.sin(i*0.3+0)*80+80), int(math.sin(i*0.3+1.5)*80+80)))
            self.customPlot.graph().setPen(pen)
            self.customPlot.graph().setName(lineNames[i-QCPGraph.lsNone])
            self.customPlot.graph().setLineStyle(QCPGraph.LineStyle(i))
            self.customPlot.graph().setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, 5))
            # generate data:
            x = [j/15.0 * 5*3.14 + 0.01 for j in range(15)]
            y = [7*math.sin(x[j])/x[j] - (i-QCPGraph.lsNone)*5 + (QCPGraph.lsImpulse)*5 + 2 for j in range(15)]
            self.customPlot.graph().setData(x, y)
            self.customPlot.graph().rescaleAxes(True)
        # zoom out a bit:
        self.customPlot.yAxis.scaleRange(1.1, self.customPlot.yAxis.range().center())
        self.customPlot.xAxis.scaleRange(1.1, self.customPlot.xAxis.range().center())
        # set blank axis lines:
        self.customPlot.xAxis.setTicks(False)
        self.customPlot.yAxis.setTicks(True)
        self.customPlot.xAxis.setTickLabels(False)
        self.customPlot.yAxis.setTickLabels(True)
        # make top right axes clones of bottom left axes:
        self.customPlot.axisRect().setupFullAxesBox()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
