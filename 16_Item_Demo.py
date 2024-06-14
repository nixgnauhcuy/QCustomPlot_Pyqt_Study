import sys, math

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtGui import QPen, QFont
from PyQt5.QtCore import Qt, QMargins, QTimer, QTime
from QCustomPlot_PyQt5 import QCustomPlot, QCP, QCPItemTracer, QCPItemPosition
from QCustomPlot_PyQt5 import QCPItemBracket, QCPItemText, QCPItemCurve, QCPLineEnding
class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Item Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.setInteractions(QCP.Interactions(QCP.iRangeDrag | QCP.iRangeZoom))
        self.customPlot.addGraph()
        n = 500
        phase = 0
        k = 3
        x = [i/(n-1)*34 - 17 for i in range(n)]
        y = [math.exp(-x[i]**2/20.0)*math.sin(k*x[i]+phase) for i in range(n)]
        self.customPlot.graph(0).setData(x, y)
        self.customPlot.graph(0).setPen(QPen(Qt.blue))
        self.customPlot.graph(0).rescaleKeyAxis()
        self.customPlot.yAxis.setRange(-1.45, 1.65)
        self.customPlot.xAxis.grid().setZeroLinePen(QPen(Qt.PenStyle.NoPen))

        # add the bracket at the top:
        self.bracket = QCPItemBracket(self.customPlot)
        self.bracket.left.setCoords(-8, 1.1)
        self.bracket.right.setCoords(8, 1.1)
        self.bracket.setLength(13)

        # add the text label at the top:
        self.wavePacketText = QCPItemText(self.customPlot)
        self.wavePacketText.position.setParentAnchor(self.bracket.center)
        self.wavePacketText.position.setCoords(0, -10) # move 10 pixels to the top from bracket center anchor
        self.wavePacketText.setPositionAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.wavePacketText.setText("Wavepacket")
        self.wavePacketText.setFont(QFont(self.font().family(), 10))

        # add the phase tracer (red circle) which sticks to the graph data (and gets updated in bracketDataSlot by timer event):
        self.phaseTracer = QCPItemTracer(self.customPlot)
        self.itemDemoPhaseTracer = self.phaseTracer # so we can access it later in the bracketDataSlot for animation
        self.phaseTracer.setGraph(self.customPlot.graph(0))
        self.phaseTracer.setGraphKey((math.pi*1.5-phase)/k)
        self.phaseTracer.setInterpolating(True)
        self.phaseTracer.setStyle(QCPItemTracer.tsCircle)
        self.phaseTracer.setPen(QPen(Qt.red))
        self.phaseTracer.setBrush(Qt.red)
        self.phaseTracer.setSize(7)

        # add label for phase tracer:
        self.phaseTracerText = QCPItemText(self.customPlot)
        self.phaseTracerText.position.setType(QCPItemPosition.ptAxisRectRatio)
        self.phaseTracerText.setPositionAlignment(Qt.AlignRight|Qt.AlignBottom)
        self.phaseTracerText.position.setCoords(1.0, 0.95) # lower right corner of axis rect
        self.phaseTracerText.setText("Points of fixed\nphase define\nphase velocity vp")
        self.phaseTracerText.setTextAlignment(Qt.AlignLeft)
        self.phaseTracerText.setFont(QFont(self.font().family(), 9))
        self.phaseTracerText.setPadding(QMargins(8, 0, 0, 0))

        # add arrow pointing at phase tracer, coming from label:
        self.phaseTracerArrow = QCPItemCurve(self.customPlot)
        self.phaseTracerArrow.start.setParentAnchor(self.phaseTracerText.left)
        self.phaseTracerArrow.startDir.setParentAnchor(self.phaseTracerArrow.start)
        self.phaseTracerArrow.startDir.setCoords(-40, 0) # direction 30 pixels to the left of parent anchor (tracerArrow->start)
        self.phaseTracerArrow.end.setParentAnchor(self.phaseTracer.position)
        self.phaseTracerArrow.end.setCoords(10, 10)
        self.phaseTracerArrow.endDir.setParentAnchor(self.phaseTracerArrow.end)
        self.phaseTracerArrow.endDir.setCoords(30, 30)
        self.phaseTracerArrow.setHead(QCPLineEnding(QCPLineEnding.esSpikeArrow))
        self.phaseTracerArrow.setTail(QCPLineEnding(QCPLineEnding.esBar, (self.phaseTracerText.bottom.pixelPosition().y()-self.phaseTracerText.top.pixelPosition().y())*0.85))

        # add the group velocity tracer (green circle):
        self.groupTracer = QCPItemTracer(self.customPlot)
        self.groupTracer.setGraph(self.customPlot.graph(0))
        self.groupTracer.setGraphKey(5.5)
        self.groupTracer.setInterpolating(True)
        self.groupTracer.setStyle(QCPItemTracer.tsCircle)
        self.groupTracer.setPen(QPen(Qt.green))
        self.groupTracer.setBrush(Qt.green)
        self.groupTracer.setSize(7)

        # add label for group tracer:
        self.groupTracerText = QCPItemText(self.customPlot)
        self.groupTracerText.position.setType(QCPItemPosition.ptAxisRectRatio)
        self.groupTracerText.setPositionAlignment(Qt.AlignRight|Qt.AlignTop)
        self.groupTracerText.position.setCoords(1.0, 0.20) # lower right corner of axis rect
        self.groupTracerText.setText("Fixed positions in\nwave packet define\ngroup velocity vg")
        self.groupTracerText.setTextAlignment(Qt.AlignLeft)
        self.groupTracerText.setFont(QFont(self.font().family(), 9))
        self.groupTracerText.setPadding(QMargins(8, 0, 0, 0))
        
        # add arrow pointing at group tracer, coming from label:
        self.groupTracerArrow = QCPItemCurve(self.customPlot)
        self.groupTracerArrow.start.setParentAnchor(self.groupTracerText.left)
        self.groupTracerArrow.startDir.setParentAnchor(self.groupTracerArrow.start)
        self.groupTracerArrow.startDir.setCoords(-40, 0) # direction 30 pixels to the left of parent anchor (tracerArrow->start)
        self.groupTracerArrow.end.setCoords(5.5, 0.4)
        self.groupTracerArrow.endDir.setParentAnchor(self.groupTracerArrow.end)
        self.groupTracerArrow.endDir.setCoords(0, -40)
        self.groupTracerArrow.setHead(QCPLineEnding(QCPLineEnding.esSpikeArrow))
        self.groupTracerArrow.setTail(QCPLineEnding(QCPLineEnding.esBar, (self.groupTracerText.bottom.pixelPosition().y()-self.groupTracerText.top.pixelPosition().y())*0.85))

        # add dispersion arrow:
        self.arrow = QCPItemCurve(self.customPlot)
        self.arrow.start.setCoords(1, -1.1)
        self.arrow.startDir.setCoords(-1, -1.3)
        self.arrow.endDir.setCoords(-5, -0.3)
        self.arrow.end.setCoords(-10, -0.2)
        self.arrow.setHead(QCPLineEnding(QCPLineEnding.esSpikeArrow))

        # add the dispersion arrow label:
        self.dispersionText = QCPItemText(self.customPlot)
        self.dispersionText.position.setCoords(-6, -0.9)
        self.dispersionText.setRotation(40)
        self.dispersionText.setText("Dispersion with\nvp < vg")
        self.dispersionText.setFont(QFont(self.font().family(), 10))

        # setup a timer that repeatedly calls MainWindow::bracketDataSlot:
        self.curTime = QTime.currentTime()
        self.dataTimer = QTimer(self)
        self.dataTimer.timeout.connect(self.bracketDataSlot)
        self.dataTimer.start(0) # Interval 0 means to refresh as fast as possible

    def bracketDataSlot(self):
        key = self.curTime.msecsTo(QTime.currentTime())/1000.0
 
        # update data to make phase move:
        n = 500
        phase = key*5
        k = 3
        x = [i/(n-1)*34 - 17 for i in range(n)]
        y = [math.exp(-x[i]**2/20.0)*math.sin(k*x[i]+phase) for i in range(n)]
        self.customPlot.graph(0).setData(x, y)
        self.itemDemoPhaseTracer.setGraphKey((8*math.pi+math.fmod(math.pi*1.5-phase, 6*math.pi))/k)
        self.customPlot.replot()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
