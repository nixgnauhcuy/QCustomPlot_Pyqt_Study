import sys

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from QCustomPlot_PyQt5 import QCustomPlot, QCPStatisticalBox, QCP, QCPAxisTickerText

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Statistical Box Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        statistical = QCPStatisticalBox(self.customPlot.xAxis, self.customPlot.yAxis)
        boxBrush = QBrush(QColor(60, 60, 255, 100))
        boxBrush.setStyle(Qt.Dense6Pattern)  # make it look oldschool
        statistical.setBrush(boxBrush)

        # specify data:
        statistical.addData(1, 1.1, 1.9, 2.25, 2.7, 4.2)
        statistical.addData(2, 0.8, 1.6, 2.2, 3.2, 4.9, [0.7, 0.34, 0.45, 6.2, 5.84])  # provide some outliers as list
        statistical.addData(3, 0.2, 0.7, 1.1, 1.6, 2.9)

        # prepare manual x axis labels:
        self.customPlot.xAxis.setSubTicks(False)
        self.customPlot.xAxis.setTickLength(0, 4)
        self.customPlot.xAxis.setTickLabelRotation(20)
        textTicker = QCPAxisTickerText()
        textTicker.addTick(1, "Sample 1")
        textTicker.addTick(2, "Sample 2")
        textTicker.addTick(3, "Control Group")
        self.customPlot.xAxis.setTicker(textTicker)

        # prepare axes:
        self.customPlot.yAxis.setLabel("O₂ Absorption [mg]")
        self.customPlot.rescaleAxes()
        self.customPlot.xAxis.scaleRange(1.7, self.customPlot.xAxis.range().center())
        self.customPlot.yAxis.setRange(0, 7)
        self.customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
