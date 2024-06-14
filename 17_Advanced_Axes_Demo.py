import sys, random, math

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtCore import Qt
from QCustomPlot_PyQt5 import QCustomPlot, QCPLayoutGrid, QCP, QCPAxis, QCPScatterStyle, QCPBars, QCPGraph
from QCustomPlot_PyQt5 import QCPAxisRect, QCPMarginGroup, QCPGraphData, QCPAxisTickerFixed
class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Advanced Axes Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        # configure axis rect:
        self.customPlot.plotLayout().clear() # clear default axis rect so we can start from scratch
        self.wideAxisRect = QCPAxisRect(self.customPlot)
        self.wideAxisRect.setupFullAxesBox(True)
        self.wideAxisRect.axis(QCPAxis.atRight, 0).setTickLabels(True)
        self.wideAxisRect.addAxis(QCPAxis.atLeft).setTickLabelColor(QColor("#6050F8")) # add an extra axis on the left and color its numbers
        self.subLayout = QCPLayoutGrid()
        self.customPlot.plotLayout().addElement(0, 0, self.wideAxisRect) # insert axis rect in first row
        self.customPlot.plotLayout().addElement(1, 0, self.subLayout) # sub layout in second row (grid layout will grow accordingly)
        # customPlot->plotLayout()->setRowStretchFactor(1, 2);
        # prepare axis rects that will be placed in the sublayout:
        self.subRectLeft = QCPAxisRect(self.customPlot, False) # false means to not setup default axes
        self.subRectRight = QCPAxisRect(self.customPlot, False)
        self.subLayout.addElement(0, 0, self.subRectLeft)
        self.subLayout.addElement(0, 1, self.subRectRight)
        self.subRectRight.setMaximumSize(150, 150) # make bottom right axis rect size fixed 150x150
        self.subRectRight.setMinimumSize(150, 150) # make bottom right axis rect size fixed 150x150
        # setup axes in sub layout axis rects:
        self.subRectLeft.addAxes(QCPAxis.atBottom | QCPAxis.atLeft)
        self.subRectRight.addAxes(QCPAxis.atBottom | QCPAxis.atRight)
        self.subRectLeft.axis(QCPAxis.atLeft).ticker().setTickCount(2)
        self.subRectRight.axis(QCPAxis.atRight).ticker().setTickCount(2)
        self.subRectRight.axis(QCPAxis.atBottom).ticker().setTickCount(2)
        self.subRectLeft.axis(QCPAxis.atBottom).grid().setVisible(True)
        # synchronize the left and right margins of the top and bottom axis rects:
        self.marginGroup = QCPMarginGroup(self.customPlot)
        self.subRectLeft.setMarginGroup(QCP.msLeft, self.marginGroup)
        self.subRectRight.setMarginGroup(QCP.msRight, self.marginGroup)
        self.wideAxisRect.setMarginGroup(QCP.msLeft | QCP.msRight, self.marginGroup)
        # move newly created axes on "axes" layer and grids on "grid" layer:
        for rect in self.customPlot.axisRects():
            for axis in rect.axes():
                axis.setLayer("axes")
                axis.grid().setLayer("grid")

        # prepare data:
        dataCos = [QCPGraphData(i/20.0*10-5.0, math.cos(i/20.0*10-5.0)) for i in range(21)]
        dataGauss = [QCPGraphData(i/50*10-5.0, math.exp(-(i/50*10-5.0)*(i/50*10-5.0)*0.2)*1000) for i in range(50)]
        dataRandom = [QCPGraphData() for i in range(100)]
        for i in range(100):
            dataRandom[i].key = i/100*10
            dataRandom[i].value = random.random()-0.5+dataRandom[max(0, i-1)].value

        x3 = [1, 2, 3, 4]
        y3 = [2, 2.5, 4, 1.5]

        # create and configure plottables:
        self.mainGraphCos = self.customPlot.addGraph(self.wideAxisRect.axis(QCPAxis.atBottom), self.wideAxisRect.axis(QCPAxis.atLeft))
        self.mainGraphCos.data().set(dataCos)
        self.mainGraphCos.valueAxis().setRange(-1, 1)
        self.mainGraphCos.rescaleKeyAxis()
        self.mainGraphCos.setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, QPen(Qt.black), QBrush(Qt.white), 6))
        self.mainGraphCos.setPen(QPen(QColor(120, 120, 120), 2))
        self.mainGraphGauss = self.customPlot.addGraph(self.wideAxisRect.axis(QCPAxis.atBottom), self.wideAxisRect.axis(QCPAxis.atLeft, 1))
        self.mainGraphGauss.data().set(dataGauss)
        self.mainGraphGauss.setPen(QPen(QColor("#8070B8"), 2))
        self.mainGraphGauss.setBrush(QColor(110, 170, 110, 30))
        self.mainGraphCos.setChannelFillGraph(self.mainGraphGauss)
        self.mainGraphCos.setBrush(QColor(255, 161, 0, 50))
        self.mainGraphGauss.valueAxis().setRange(0, 1000)
        self.mainGraphGauss.rescaleKeyAxis()

        self.subGraphRandom = self.customPlot.addGraph(self.subRectLeft.axis(QCPAxis.atBottom), self.subRectLeft.axis(QCPAxis.atLeft))
        self.subGraphRandom.data().set(dataRandom)
        self.subGraphRandom.setLineStyle(QCPGraph.lsImpulse)
        self.subGraphRandom.setPen(QPen(QColor("#FFA100"), 1.5))
        self.subGraphRandom.rescaleAxes()

        self.subBars = QCPBars(self.subRectRight.axis(QCPAxis.atBottom), self.subRectRight.axis(QCPAxis.atRight))
        self.subBars.setWidth(3/len(x3))
        self.subBars.setData(x3, y3)
        self.subBars.setPen(QPen(Qt.black))
        self.subBars.setAntialiased(False)
        self.subBars.setAntialiasedFill(False)
        self.subBars.setBrush(QColor("#705BE8"))
        self.subBars.keyAxis().setSubTicks(False)
        self.subBars.rescaleAxes()
        # setup a ticker for subBars key axis that only gives integer ticks:
        intTicker = QCPAxisTickerFixed()
        intTicker.setTickStep(1.0)
        intTicker.setScaleStrategy(QCPAxisTickerFixed.ssMultiples)
        self.subBars.keyAxis().setTicker(intTicker)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
