import sys, math

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from QCustomPlot_PyQt5 import QCustomPlot, QCPAxis, QCPColorScale, QCPColorMap
from QCustomPlot_PyQt5 import QCPColorGradient, QCPMarginGroup, QCP, QCPRange

class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Color Map Demo")
        self.resize(600,400)

        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        # configure axis rect:
        self.customPlot.setInteractions(QCP.Interactions(QCP.iRangeDrag | QCP.iRangeZoom)) # this will also allow rescaling the color scale by dragging/zooming
        self.customPlot.axisRect().setupFullAxesBox(True)
        self.customPlot.xAxis.setLabel("x")
        self.customPlot.yAxis.setLabel("y")

        # set up the QCPColorMap:
        self.colorMap = QCPColorMap(self.customPlot.xAxis, self.customPlot.yAxis)
        nx = 200
        ny = 200
        self.colorMap.data().setSize(nx, ny) # we want the color map to have nx * ny data points
        self.colorMap.data().setRange(QCPRange(-4, 4), QCPRange(-4, 4)) # and span the coordinate range -4..4 in both key (x) and value (y) dimensions
        # now we assign some data, by accessing the QCPColorMapData instance of the color map:
        x, y, z = 0, 0, 0
        for xIndex in range(nx):
            for yIndex in range(ny):
                x, y =self.colorMap.data().cellToCoord(xIndex, yIndex)
                r = 3*math.sqrt(x*x+y*y)+1e-2
                z = 2*x*(math.cos(r+2)/r-math.sin(r+2)/r) # the B field strength of dipole radiation (modulo physical constants)
                self.colorMap.data().setCell(xIndex, yIndex, z)
        # add a color scale:
        self.colorScale = QCPColorScale(self.customPlot)
        self.customPlot.plotLayout().addElement(0, 1, self.colorScale) # add it to the right of the main axis rect
        self.colorScale.setType(QCPAxis.atRight) # scale shall be vertical bar with tick/axis labels right (actually atRight is already the default)
        self.colorMap.setColorScale(self.colorScale) # associate the color map with the color scale
        self.colorScale.axis().setLabel("Magnetic Field Strength")

        # set the color gradient of the color map to one of the presets:
        self.colorMap.setGradient(QCPColorGradient(QCPColorGradient.gpPolar))
        # we could have also created a QCPColorGradient instance and added own colors to
        # the gradient, see the documentation of QCPColorGradient for what's possible.

        self.colorMap.rescaleDataRange() 

        # make sure the axis rect and color scale synchronize their bottom and top margins (so they line up):
        marginGroup = QCPMarginGroup(self.customPlot)
        self.customPlot.axisRect().setMarginGroup(QCP.msBottom|QCP.msTop, marginGroup)
        self.colorScale.setMarginGroup(QCP.msBottom|QCP.msTop, marginGroup)

        # rescale the key (x) and value (y) axes so the whole color map is visible:
        self.customPlot.rescaleAxes()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
