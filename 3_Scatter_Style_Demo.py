import sys, math

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor, QFont, QPainterPath
from PyQt5.QtCore import Qt
from QCustomPlot_PyQt5 import QCustomPlot, QCPGraph, QCPScatterStyle

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Scatter Style Demo")
        self.resize(400,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.legend.setVisible(True)
        self.customPlot.legend.setFont(QFont("Helvetica", 9))
        self.customPlot.legend.setRowSpacing(-3)

        shapes = [
            QCPScatterStyle.ssCross, 
            QCPScatterStyle.ssPlus, 
            QCPScatterStyle.ssCircle, 
            QCPScatterStyle.ssDisc, 
            QCPScatterStyle.ssSquare, 
            QCPScatterStyle.ssDiamond, 
            QCPScatterStyle.ssStar, 
            QCPScatterStyle.ssTriangle, 
            QCPScatterStyle.ssTriangleInverted, 
            QCPScatterStyle.ssCrossSquare, 
            QCPScatterStyle.ssPlusSquare, 
            QCPScatterStyle.ssCrossCircle, 
            QCPScatterStyle.ssPlusCircle, 
            QCPScatterStyle.ssPeace, 
            QCPScatterStyle.ssCustom
        ]
        shapes_names = [
            "ssCross",
            "ssPlus",
            "ssCircle",
            "ssDisc",
            "ssSquare",
            "ssDiamond",
            "ssStar",
            "ssTriangle",
            "ssTriangleInverted",
            "ssCrossSquare",
            "ssPlusSquare",
            "ssCrossCircle",
            "ssPlusCircle",
            "ssPeace",
            "ssCustom"
        ]

        self.pen = QPen()
        # add graphs with different scatter styles:
        for i in range(len(shapes)):
            self.customPlot.addGraph()
            self.pen.setColor(QColor(int(math.sin(i*0.3)*100+100), int(math.sin(i*0.6+0.7)*100+100), int(math.sin(i*0.4+0.6)*100+100)))

            # generate data:
            x = [k/10.0 * 4*3.14 + 0.01 for k in range(10)]
            y = [7*math.sin(x[k])/x[k] + (len(shapes)-i)*5 for k in range(10)]

            self.customPlot.graph(i).setData(x, y)
            self.customPlot.graph(i).rescaleAxes(True)
            self.customPlot.graph(i).setPen(self.pen)
            self.customPlot.graph(i).setName(shapes_names[i])
            self.customPlot.graph(i).setLineStyle(QCPGraph.lsLine)

            # set scatter style:
            if shapes[i] != QCPScatterStyle.ssCustom:
                self.customPlot.graph(i).setScatterStyle(QCPScatterStyle(shapes[i], 10))
            else:
                customScatterPath = QPainterPath()
                for j in range(3):
                    customScatterPath.cubicTo(math.cos(2*math.pi*j/3.0)*9, math.sin(2*math.pi*j/3.0)*9, math.cos(2*math.pi*(j+0.9)/3.0)*9, math.sin(2*math.pi*(j+0.9)/3.0)*9, 0, 0)
                self.customPlot.graph(i).setScatterStyle(QCPScatterStyle(customScatterPath, QPen(Qt.black, 0), QColor(40, 70, 255, 50), 10))

        # set blank axis lines:
        self.customPlot.rescaleAxes()
        self.customPlot.xAxis.setTicks(False)
        self.customPlot.yAxis.setTicks(False)
        self.customPlot.xAxis.setTickLabels(False)
        self.customPlot.yAxis.setTickLabels(False)

        # make top right axes clones of bottom left axes:
        self.customPlot.axisRect().setupFullAxesBox()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
