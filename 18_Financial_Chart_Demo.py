import sys, random

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import Qt, QDateTime, QDate, QMargins
from QCustomPlot_PyQt5 import QCustomPlot, QCPFinancial, QCP, QCPAxis, QCPBars
from QCustomPlot_PyQt5 import QCPAxisRect, QCPMarginGroup, QCPAxisTickerDateTime
class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Financial Chart Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.legend.setVisible(True)

        # generate two sets of random walk data (one for candlestick and one for ohlc chart):
        n = 500
        start = QDateTime(QDate(2014, 6, 11))
        start.setTimeSpec(Qt.UTC)
        startTime = start.toTime_t()
        binSize = 3600*24 # bin data in 1 day intervals
        time = [startTime + 3600*i for i in range(n)]
        value1 = [0 for i in range(n)]
        value1[0] = 60
        value2 = [0 for i in range(n)]
        value2[0] = 20
        for i in range(1, n):
            value1[i] = value1[i-1] + (random.random()-0.5)*10
            value2[i] = value2[i-1] + (random.random()-0.5)*3
        
        # create candlestick chart:
        candlesticks = QCPFinancial(self.customPlot.xAxis, self.customPlot.yAxis)
        candlesticks.setName("Candlestick")
        candlesticks.setChartStyle(QCPFinancial.csCandlestick)
        candlesticks.data().set(QCPFinancial.timeSeriesToOhlc(time, value1, binSize, startTime))
        candlesticks.setWidth(binSize*0.9)
        candlesticks.setTwoColored(True)
        candlesticks.setBrushPositive(QColor(245, 245, 245))
        candlesticks.setBrushNegative(QColor(40, 40, 40))
        candlesticks.setPenPositive(QPen(QColor(0, 0, 0)))
        candlesticks.setPenNegative(QPen(QColor(0, 0, 0)))

        # create ohlc chart:
        ohlc = QCPFinancial(self.customPlot.xAxis, self.customPlot.yAxis)
        ohlc.setName("OHLC")
        ohlc.setChartStyle(QCPFinancial.csOhlc)
        ohlc.data().set(QCPFinancial.timeSeriesToOhlc(time, value2, binSize/3.0, startTime)) # divide binSize by 3 just to make the ohlc bars a bit denser
        ohlc.setWidth(binSize*0.2)
        ohlc.setTwoColored(True)

        # create bottom axis rect for volume bar chart:
        volumeAxisRect = QCPAxisRect(self.customPlot)
        self.customPlot.plotLayout().addElement(1, 0, volumeAxisRect)
        volumeAxisRect.setMaximumSize(16777215, 100)
        volumeAxisRect.axis(QCPAxis.atBottom).setLayer("axes")
        volumeAxisRect.axis(QCPAxis.atBottom).grid().setLayer("grid")
        # bring bottom and main axis rect closer together:
        self.customPlot.plotLayout().setRowSpacing(0)
        volumeAxisRect.setAutoMargins(QCP.MarginSides(QCP.msLeft|QCP.msRight|QCP.msBottom))
        volumeAxisRect.setMargins(QMargins(0, 0, 0, 0))
        # create two bar plottables, for positive (green) and negative (red) volume bars:
        self.customPlot.setAutoAddPlottableToLegend(False)
        volumePos = QCPBars(volumeAxisRect.axis(QCPAxis.atBottom), volumeAxisRect.axis(QCPAxis.atLeft))
        volumeNeg = QCPBars(volumeAxisRect.axis(QCPAxis.atBottom), volumeAxisRect.axis(QCPAxis.atLeft))
        for i in range(n//5):
            v = random.randint(-20000, 20000)
            if v < 0:
                volumeNeg.addData(startTime+3600*5.0*i, abs(v))
            else:
                volumePos.addData(startTime+3600*5.0*i, abs(v))
        volumePos.setWidth(3600*4)
        volumePos.setPen(QPen(Qt.PenStyle.NoPen))
        volumePos.setBrush(QColor(100, 180, 110))
        volumeNeg.setWidth(3600*4)
        volumeNeg.setPen(QPen(Qt.PenStyle.NoPen))
        volumeNeg.setBrush(QColor(180, 90, 90))

        # interconnect x axis ranges of main and bottom axis rects:
        self.customPlot.xAxis.rangeChanged.connect(volumeAxisRect.axis(QCPAxis.atBottom).setRange)
        volumeAxisRect.axis(QCPAxis.atBottom).rangeChanged.connect(self.customPlot.xAxis.setRange)
        # configure axes of both main and bottom axis rect:
        dateTimeTicker = QCPAxisTickerDateTime()
        dateTimeTicker.setDateTimeSpec(Qt.UTC)
        dateTimeTicker.setDateTimeFormat("dd. MMMM")
        volumeAxisRect.axis(QCPAxis.atBottom).setTicker(dateTimeTicker)
        volumeAxisRect.axis(QCPAxis.atBottom).setTickLabelRotation(15)
        self.customPlot.xAxis.setBasePen(QPen(Qt.PenStyle.NoPen))
        self.customPlot.xAxis.setTickLabels(False)
        self.customPlot.xAxis.setTicks(False) # only want vertical grid in main axis rect, so hide xAxis backbone, ticks, and labels
        self.customPlot.xAxis.setTicker(dateTimeTicker)
        self.customPlot.rescaleAxes()
        self.customPlot.xAxis.scaleRange(1.025, self.customPlot.xAxis.range().center())
        self.customPlot.yAxis.scaleRange(1.1, self.customPlot.yAxis.range().center())
        
        # make axis rects' left side line up:
        group = QCPMarginGroup(self.customPlot)
        self.customPlot.axisRect().setMarginGroup(QCP.msLeft|QCP.msRight, group)
        volumeAxisRect.setMarginGroup(QCP.msLeft|QCP.msRight, group)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
