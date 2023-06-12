import numpy
import matplotlib.pyplot as graph
from matplotlib import style

style.use('bmh')

class Graph2D:
    x_values = None
    y_values = None
    title = str()
    x_title = str()
    y_title = str()

    def __init__(self, x_values: list, y_values: list, title = '', x_title = '', y_title = ''):
        self.x_values = numpy.array(x_values)
        self.y_values = numpy.array(y_values)
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        graph.title(self.title)
        graph.xlabel(self.x_title)
        graph.ylabel(self.y_title)

    def scatterPlot(self):
        graph.scatter(self.x_values, self.y_values, marker = 'x', c = 'r')
        graph.show()

    def lineGraph(self):
        graph.plot(self.x_values, self.y_values, c = 'r')
        graph.show()