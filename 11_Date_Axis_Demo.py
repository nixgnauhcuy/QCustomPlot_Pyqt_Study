import sys, math, random

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QColor, QBrush, QFont
from PyQt5.QtCore import QDateTime, QLocale
from QCustomPlot_PyQt5 import QCustomPlot, QCPGraph, QCPGraphData, QCPAxisTickerText, QCPAxisTickerDateTime

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Date Axis Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        # set locale to english, so we get english month names:
        self.customPlot.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        # seconds of current time, we'll use it as starting point in time for data:
        self.now = QDateTime.currentDateTime().toTime_t()
        # create multiple graphs:
        for i in range(5):
            self.customPlot.addGraph()
            color = QColor(int(20+200/4.0*i), int(70*(1.6-i/4.0)), 150, 150)
            self.customPlot.graph().setLineStyle(QCPGraph.lsLine)
            self.customPlot.graph().setPen(QPen(color.lighter(200)))
            self.customPlot.graph().setBrush(QBrush(color))

            # generate random walk data:
            timeData = [QCPGraphData() for k in range(250)]
            for j in range(250):
                timeData[j].key = self.now + 24*3600*j
                if j == 0:
                    timeData[j].value = (j/50.0+1)*(random.random()/5.0-0.5)
                else:
                    timeData[j].value = math.fabs(timeData[j-1].value)*(1+0.02/4.0*(4-i)) + (j/50.0+1)*(random.random()-0.5)
            self.customPlot.graph().data().set(timeData)

        # configure bottom axis to show date instead of number:
        dateTicker = QCPAxisTickerDateTime()
        dateTicker.setDateTimeFormat("d. MMMM\nyyyy")
        self.customPlot.xAxis.setTicker(dateTicker)

        # configure left axis text labels:
        textTicker = QCPAxisTickerText()
        textTicker.addTick(10, "a bit\nlow")
        textTicker.addTick(50, "quite\nhigh")
        self.customPlot.yAxis.setTicker(textTicker)

        # set a more compact font size for bottom and left axis tick labels:
        self.customPlot.xAxis.setTickLabelFont(QFont(QFont().family(), 8))
        self.customPlot.yAxis.setTickLabelFont(QFont(QFont().family(), 8))

        # set axis labels:
        self.customPlot.xAxis.setLabel("Date")
        self.customPlot.yAxis.setLabel("Random wobbly lines value")

        # make top and right axes visible but without ticks and labels:
        self.customPlot.xAxis2.setVisible(True)
        self.customPlot.yAxis2.setVisible(True)
        self.customPlot.xAxis2.setTicks(False)
        self.customPlot.yAxis2.setTicks(False)
        self.customPlot.xAxis2.setTickLabels(False)
        self.customPlot.yAxis2.setTickLabels(False)

        # set axis ranges to show all data:
        self.customPlot.xAxis.setRange(self.now, self.now+24*3600*249)
        self.customPlot.yAxis.setRange(0, 60)

        # show legend with slightly transparent background brush:
        self.customPlot.legend.setVisible(True)
        self.customPlot.legend.setBrush(QColor(255, 255, 255, 150))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
