import sys

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor, QFont, QBrush, QPixmap
from PyQt5.QtCore import Qt

from QCustomPlot_PyQt5 import QCustomPlot, QCPTextElement, QCPScatterStyle, QCPGraph

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Scatter Pixmap Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.axisRect().setBackground(QColor(0, 0, 0))
        self.customPlot.addGraph()
        self.customPlot.graph().setLineStyle(QCPGraph.lsLine)
        pen = QPen(QColor(255, 200, 20, 200))
        pen.setStyle(Qt.DashLine)
        pen.setWidthF(2.5)
        self.customPlot.graph().setPen(pen)
        self.customPlot.graph().setBrush(QBrush(QColor(255,200,20,70)))
        self.customPlot.graph().setScatterStyle(QCPScatterStyle(QPixmap("./img/sun.png")))

        # set graph name, will show up in legend next to icon:
        self.customPlot.graph().setName("Data from Photovoltaic\nenergy barometer 2011")
        # set data:
        year = [2005, 2006, 2007, 2008, 2009, 2010, 2011]
        value = [2.17, 3.42, 4.94, 10.38, 15.86, 29.33, 52.1]
        self.customPlot.graph().setData(year, value)

        # set title of plot:
        self.customPlot.plotLayout().insertRow(0)
        self.customPlot.plotLayout().addElement(0, 0, QCPTextElement(self.customPlot, "Regenerative Energies", QFont("sans", 12, QFont.Bold)))
        # axis configurations:
        self.customPlot.xAxis.setLabel("Year")
        self.customPlot.yAxis.setLabel("Installed Gigawatts of\nphotovoltaic in the European Union")
        self.customPlot.xAxis2.setVisible(True)
        self.customPlot.yAxis2.setVisible(True)
        self.customPlot.xAxis2.setTickLabels(False)
        self.customPlot.yAxis2.setTickLabels(False)
        self.customPlot.xAxis2.setTicks(False)
        self.customPlot.yAxis2.setTicks(False)
        self.customPlot.xAxis2.setSubTicks(False)
        self.customPlot.yAxis2.setSubTicks(False)
        self.customPlot.xAxis.setRange(2004.5, 2011.5)
        self.customPlot.yAxis.setRange(0, 52)
        # setup legend:
        self.customPlot.legend.setFont(QFont(self.font().family(), 7))
        self.customPlot.legend.setIconSize(50, 20)
        self.customPlot.legend.setVisible(True)
        self.customPlot.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignLeft | Qt.AlignTop)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
