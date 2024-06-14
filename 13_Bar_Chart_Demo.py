import sys

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor, QBrush, QFont, QLinearGradient
from PyQt5.QtCore import Qt
from QCustomPlot_PyQt5 import QCustomPlot, QCPBars, QCP, QCPAxisTickerText

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Bar Chart Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        # set dark background gradient:
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor(90, 90, 90))
        gradient.setColorAt(0.38, QColor(105, 105, 105))
        gradient.setColorAt(1, QColor(70, 70, 70))
        self.customPlot.setBackground(QBrush(gradient))

        # create empty bar chart objects:
        self.regen = QCPBars(self.customPlot.xAxis, self.customPlot.yAxis)
        self.nuclear = QCPBars(self.customPlot.xAxis, self.customPlot.yAxis)
        self.fossil = QCPBars(self.customPlot.xAxis, self.customPlot.yAxis)
        self.regen.setAntialiased(False) # gives more crisp, pixel aligned bar borders
        self.nuclear.setAntialiased(False)
        self.fossil.setAntialiased(False)
        self.regen.setStackingGap(1)
        self.nuclear.setStackingGap(1)
        self.fossil.setStackingGap(1)
        # set names and colors:
        self.fossil.setName("Fossil fuels")
        self.fossil.setPen(QPen(QColor(111, 9, 176).lighter(170)))
        self.fossil.setBrush(QColor(111, 9, 176))
        self.nuclear.setName("Nuclear")
        self.nuclear.setPen(QPen(QColor(250, 170, 20).lighter(150)))
        self.nuclear.setBrush(QColor(250, 170, 20))
        self.regen.setName("Regenerative")
        self.regen.setPen(QPen(QColor(0, 168, 140).lighter(130)))
        self.regen.setBrush(QColor(0, 168, 140))
        # stack bars on top of each other:
        self.nuclear.moveAbove(self.fossil)
        self.regen.moveAbove(self.nuclear)

        # prepare x axis with country labels:
        ticks = [1, 2, 3, 4, 5, 6, 7]
        labels = ["USA", "Japan", "Germany", "France", "UK", "Italy", "Canada"]
        textTicker = QCPAxisTickerText()
        textTicker.addTicks(ticks, labels)
        self.customPlot.xAxis.setTicker(textTicker)
        self.customPlot.xAxis.setTickLabelRotation(60)
        self.customPlot.xAxis.setSubTicks(False)
        self.customPlot.xAxis.setTickLength(0, 4)
        self.customPlot.xAxis.setRange(0, 8)
        self.customPlot.xAxis.setBasePen(QPen(Qt.white))
        self.customPlot.xAxis.setTickPen(QPen(Qt.white))
        self.customPlot.xAxis.grid().setVisible(True)
        self.customPlot.xAxis.grid().setPen(QPen(QColor(130, 130, 130), 0, Qt.DotLine))
        self.customPlot.xAxis.setTickLabelColor(Qt.white)
        self.customPlot.xAxis.setLabelColor(Qt.white)

        # prepare y axis:
        self.customPlot.yAxis.setRange(0, 12.1)
        self.customPlot.yAxis.setPadding(5) # a bit more space to the left border
        self.customPlot.yAxis.setLabel("Power Consumption in\nKilowatts per Capita (2007)")
        self.customPlot.yAxis.setBasePen(QPen(Qt.white))
        self.customPlot.yAxis.setTickPen(QPen(Qt.white))
        self.customPlot.yAxis.setSubTickPen(QPen(Qt.white))
        self.customPlot.yAxis.grid().setSubGridVisible(True)
        self.customPlot.yAxis.setTickLabelColor(Qt.white)
        self.customPlot.yAxis.setLabelColor(Qt.white)
        self.customPlot.yAxis.grid().setPen(QPen(QColor(130, 130, 130), 0, Qt.SolidLine))
        self.customPlot.yAxis.grid().setSubGridPen(QPen(QColor(130, 130, 130), 0, Qt.DotLine))

        # Add data:
        self.fossilData  = [0.86*10.5, 0.83*5.5, 0.84*5.5, 0.52*5.8, 0.89*5.2, 0.90*4.2, 0.67*11.2]
        self.nuclearData = [0.08*10.5, 0.12*5.5, 0.40*5.8, 0.09*5.2, 0.00*4.2, 0.07*11.2]
        self.regenData   = [0.06*10.5, 0.05*5.5, 0.04*5.5, 0.06*5.8, 0.02*5.2, 0.07*4.2, 0.25*11.2]
        self.fossil.setData(ticks, self.fossilData)
        self.nuclear.setData(ticks, self.nuclearData)
        self.regen.setData(ticks, self.regenData)

        # setup legend:
        self.customPlot.legend.setVisible(True)
        self.customPlot.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignTop|Qt.AlignHCenter)
        self.customPlot.legend.setBrush(QColor(255, 255, 255, 100))
        self.customPlot.legend.setBorderPen(QPen(Qt.PenStyle.NoPen))
        legendFont = QFont()
        legendFont.setPointSize(10)
        self.customPlot.legend.setFont(legendFont)
        self.customPlot.setInteractions(QCP.Interactions(QCP.iRangeDrag | QCP.iRangeZoom))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
