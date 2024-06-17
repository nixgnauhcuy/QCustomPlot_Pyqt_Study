import sys, math, random

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMenu, QLineEdit, QInputDialog
from PyQt5.QtGui import QPen, QFont, QColor
from PyQt5.QtCore import Qt
from QCustomPlot_PyQt5 import QCustomPlot, QCP, QCPScatterStyle, QCPGraph, QCPAxis
from QCustomPlot_PyQt5 import QCPTextElement, QCPLegend, QCPDataSelection
class MainForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Interaction Example")
        self.resize(600,400)

        self.mousePos = 0
        self.customPlot = QCustomPlot(self)
        self.gridLayout = QGridLayout(self).addWidget(self.customPlot)

        self.customPlot.setInteractions(QCP.Interactions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectAxes | QCP.iSelectLegend | QCP.iSelectPlottables))
        self.customPlot.xAxis.setRange(-8, 8)
        self.customPlot.yAxis.setRange(-5, 5)
        self.customPlot.axisRect().setupFullAxesBox()

        self.customPlot.plotLayout().insertRow(0)
        self.title = QCPTextElement(self.customPlot, "Interaction Example", QFont("sans", 17, QFont.Bold))
        self.customPlot.plotLayout().addElement(0, 0, self.title)

        self.customPlot.xAxis.setLabel("x Axis")
        self.customPlot.yAxis.setLabel("y Axis")
        self.customPlot.legend.setVisible(True)
        legendFont = QFont()
        legendFont.setPointSize(10)
        self.customPlot.legend.setFont(legendFont)
        self.customPlot.legend.setSelectedFont(legendFont)
        self.customPlot.legend.setSelectableParts(QCPLegend.spItems) # legend box shall not be selectable, only legend items

        self.addRandomGraph()
        self.addRandomGraph()
        self.addRandomGraph()
        self.addRandomGraph()
        self.customPlot.rescaleAxes()
        
        # connect slot that ties some axis selections together (especially opposite axes):
        self.customPlot.selectionChangedByUser.connect(self.selectionChanged)
        # connect slots that takes care that when an axis is selected, only that direction can be dragged and zoomed:
        self.customPlot.mousePress.connect(self.mousePressCb)
        self.customPlot.mouseWheel.connect(self.mouseWheelCb)

        # make bottom and left axes transfer their ranges to top and right axes:
        self.customPlot.xAxis.rangeChanged.connect(lambda: self.customPlot.xAxis2.setRange(self.customPlot.xAxis2.range()))
        self.customPlot.yAxis.rangeChanged.connect(lambda: self.customPlot.yAxis2.setRange(self.customPlot.yAxis2.range()))

        # connect some interaction slots:
        self.customPlot.axisDoubleClick.connect(self.axisLabelDoubleClick)
        self.customPlot.legendDoubleClick.connect(self.legendDoubleClick)
        self.title.doubleClicked.connect(self.titleDoubleClick)

        # connect slot that shows a message in the status bar when a graph is clicked:
        self.customPlot.plottableClick.connect(self.graphClicked)

        # setup policy and connect slot for context menu popup:
        self.customPlot.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customPlot.customContextMenuRequested.connect(self.contextMenuRequest)

    def addRandomGraph(self):
        n = 50 # number of points in graph
        xScale = (random.random() + 0.5)*2
        yScale = (random.random() + 0.5)*2
        xOffset = (random.random() - 0.5)*4
        yOffset = (random.random() - 0.5)*10
        r1 = (random.random() - 0.5)*2
        r2 = (random.random() - 0.5)*2
        r3 = (random.random() - 0.5)*2
        r4 = (random.random() - 0.5)*2
        x = [i/(n-0.5)*10.0*xScale + xOffset for i in range(n)]
        y = [(math.sin(x[i]*r1*5)*math.sin(math.cos(x[i]*r2)*r4*3)+r3*math.cos(math.sin(x[i])*r4*2))*yScale + yOffset for i in range(n)]
        self.customPlot.addGraph()
        self.customPlot.graph().setName(f"New Graph {self.customPlot.graphCount()-1}")
        self.customPlot.graph().setData(x, y)

        self.customPlot.graph().setLineStyle((QCPGraph.LineStyle)(math.floor(random.random()*5)+1))
        if (math.floor(random.random()*100) > 50):
            self.customPlot.graph().setScatterStyle(QCPScatterStyle((QCPScatterStyle.ScatterShape)(math.floor(random.random()*14)+1)))

        graphPen = QPen()
        graphPen.setColor(QColor(math.floor(random.random()*245+10), math.floor(random.random()*245+10), math.floor(random.random()*245+10)))
        graphPen.setWidthF(random.random()/(random.random()*2+1))
        self.customPlot.graph().setPen(graphPen)
        self.customPlot.graph().setBrush(QColor(int(random.random()*255), int(random.random()*255), int(random.random()*255), 20))
        self.customPlot.replot()


    def selectionChanged(self):
        # normally, axis base line, axis tick labels and axis labels are selectable separately, but we want
        # the user only to be able to select the axis as a whole, so we tie the selected states of the tick labels
        # and the axis base line together. However, the axis label shall be selectable individually.

        # The selection state of the left and right axes shall be synchronized as well as the state of the
        # bottom and top axes.

        # Further, we want to synchronize the selection of the graphs with the selection state of the respective
        # legend item belonging to that graph. So the user can select a graph by either clicking on the graph itself
        # or on its legend item.

        # make top and bottom axes be selected synchronously, and handle axis and tick labels as one selectable object:
        if (self.customPlot.xAxis.getPartAt(self.mousePos) == QCPAxis.spAxis or self.customPlot.xAxis.getPartAt(self.mousePos) == QCPAxis.spTickLabels or
            self.customPlot.xAxis2.getPartAt(self.mousePos) == QCPAxis.spAxis or self.customPlot.xAxis2.getPartAt(self.mousePos) == QCPAxis.spTickLabels):
            self.customPlot.xAxis2.setSelectedParts(QCPAxis.spAxis|QCPAxis.spTickLabels)
            self.customPlot.xAxis.setSelectedParts(QCPAxis.spAxis|QCPAxis.spTickLabels)

        # make left and right axes be selected synchronously, and handle axis and tick labels as one selectable object:
        if (self.customPlot.yAxis.getPartAt(self.mousePos) == QCPAxis.spAxis or self.customPlot.yAxis.getPartAt(self.mousePos) == QCPAxis.spTickLabels or
            self.customPlot.yAxis2.getPartAt(self.mousePos) == QCPAxis.spAxis or self.customPlot.yAxis2.getPartAt(self.mousePos) == QCPAxis.spTickLabels):
            self.customPlot.yAxis2.setSelectedParts(QCPAxis.spAxis|QCPAxis.spTickLabels)
            self.customPlot.yAxis.setSelectedParts(QCPAxis.spAxis|QCPAxis.spTickLabels)

        # synchronize selection of graphs with selection of corresponding legend items:
        for i in range(self.customPlot.graphCount()):
            graph = self.customPlot.graph(i)
            item = self.customPlot.legend.itemWithPlottable(graph)
            if (item.selected() or graph.selected()):
                item.setSelected(True)
                graph.setSelection(QCPDataSelection(graph.data().dataRange()))
   
    def mousePressCb(self, event):
        # if an axis is selected, only allow the direction of that axis to be dragged
        # if no axis is selected, both directions may be dragged

        self.mousePos = event.pos()

        if self.customPlot.xAxis.getPartAt(event.pos()) == QCPAxis.spAxis:
            self.customPlot.axisRect().setRangeDrag(self.customPlot.xAxis.orientation())
        elif self.customPlot.yAxis.getPartAt(event.pos()) == QCPAxis.spAxis:
            self.customPlot.axisRect().setRangeDrag(self.customPlot.yAxis.orientation())
        else:
            self.customPlot.axisRect().setRangeDrag(Qt.Horizontal|Qt.Vertical)
    
    def mouseWheelCb(self, event):
        # if an axis is selected, only allow the direction of that axis to be zoomed
        # if no axis is selected, both directions may be zoomed

        if self.customPlot.xAxis.getPartAt(event.pos())  == QCPAxis.spAxis:
            self.customPlot.axisRect().setRangeZoom(self.customPlot.xAxis.orientation())
        elif self.customPlot.yAxis.getPartAt(event.pos())  == QCPAxis.spAxis:
            self.customPlot.axisRect().setRangeZoom(self.customPlot.yAxis.orientation())
        else:
            self.customPlot.axisRect().setRangeZoom(Qt.Horizontal|Qt.Vertical)


    def removeSelectedGraph(self):
        if len(self.customPlot.selectedGraphs()) > 0:
            self.customPlot.removeGraph(self.customPlot.selectedGraphs()[0])
            self.customPlot.replot()
 
    def removeAllGraphs(self):
        self.customPlot.clearGraphs()
        self.customPlot.replot()

    def moveLegend(self, alignment):
        self.customPlot.axisRect().insetLayout().setInsetAlignment(0, alignment)
        self.customPlot.replot()


    def contextMenuRequest(self, pos):
        menu = QMenu(self)
        menu.setAttribute(Qt.WA_DeleteOnClose)
        if self.customPlot.legend.selectTest(pos, False) >= 0: # context menu on legend requested
            menu.addAction("Move to top left", lambda: self.moveLegend(Qt.AlignTop|Qt.AlignLeft))
            menu.addAction("Move to top center", lambda: self.moveLegend(Qt.AlignTop|Qt.AlignHCenter))
            menu.addAction("Move to top right", lambda: self.moveLegend(Qt.AlignTop|Qt.AlignRight))
            menu.addAction("Move to bottom right", lambda: self.moveLegend(Qt.AlignBottom|Qt.AlignRight))
            menu.addAction("Move to bottom left", lambda: self.moveLegend(Qt.AlignBottom|Qt.AlignLeft))
        else: # general context menu on graphs requested
            menu.addAction("Add random graph", self.addRandomGraph)
            if len(self.customPlot.selectedGraphs()) > 0:
                menu.addAction("Remove selected graph", self.removeSelectedGraph)
            if self.customPlot.graphCount() > 0:
                menu.addAction("Remove all graphs", self.removeAllGraphs)
        menu.popup(self.customPlot.mapToGlobal(pos))

    def axisLabelDoubleClick(self, axis, part):
        # Set an axis label by double clicking on it
        if part == QCPAxis.spAxisLabel: # only react when the actual axis label is clicked, not tick label or axis backbone
            newLabel, ok = QInputDialog.getText(self, "QCustomPlot example", "New axis label:", QLineEdit.Normal, axis.label())
            if ok:
                axis.setLabel(newLabel)
                self.customPlot.replot()

    def legendDoubleClick(self, legend, item):
        # Rename a graph by double clicking on its legend item
        if item: # only react if item was clicked (user could have clicked on border padding of legend where there is no item, then item is 0)
            plItem = item.plottable()
            newName, ok = QInputDialog.getText(self, "QCustomPlot example", "New graph name:", QLineEdit.Normal, plItem.name())
            if ok:
                plItem.setName(newName)
                self.customPlot.replot()

    def titleDoubleClick(self, event):
        # Set the plot title by double clicking on it
        newTitle, ok = QInputDialog.getText(self, "QCustomPlot example", "New plot title:", QLineEdit.Normal, self.title.text())
        if ok:
            self.title.setText(newTitle)
            self.customPlot.replot()
    
    def graphClicked(self, plottable, dataIndex):
        # since we know we only have QCPGraphs in the plot, we can immediately access interface1D()
        # usually it's better to first check whether interface1D() returns non-zero, and only then use it.
        dataValue = plottable.interface1D().dataMainValue(dataIndex)
        message = f"Clicked on graph '{plottable.name()}' at data point #{dataIndex} with value {dataValue}."
        print(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec())
