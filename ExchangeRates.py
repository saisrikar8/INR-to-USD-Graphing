import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from Graph import Graph2D
from DataSet import DataSetElement


class ExchangeRate:
    year = int()
    rates = dict()

    def __init__(self, year):
        self.year = year
        self.rates = self.getExchangeRatesByDay(self, year)
    def getExchangeRatesByDay(newYear):
        url = 'https://www.exchangerates.org.uk/INR-USD-spot-exchange-rates-history-'+ str(newYear) + '.html'
        website = urllib.request.urlopen(url)
        soup = BeautifulSoup(website, 'html.parser')
        tableRows = list(soup('tr')[1:])
        points = {}
        for row in tableRows:
            if row.attrs.get('class') is None:
                continue
            rowList = list(row.children)
            date = rowList[0].text.split()
            month = date[2]
            day = int(date[1])

            rate = float(rowList[1].text.split(' = $')[1])
            if points.get(month) is None:
                points[month] = dict()

            points[month][day] = rate
        return points
    def getMonthAvgValues(self):
        avgVals = []
        for month in self.rates:
            monthSum = 0.0
            length = 0
            monthDict = self.rates[month]
            for day in monthDict:
                monthSum += monthDict[day]
                length += 1
            monthAvg = monthSum / length
            avgVals.append(monthAvg)
        return avgVals

    def getMonthEndValues(self):
        endVals = []
        for month in self.rates:
            endVals.append(self.rates[month][len(self.rates[month])])
        return endVals

    def getMonthBeginValues(self):
        beginVals = []
        for month in self.rates:
            beginVals.append(self.rates[month][1])
        return beginVals

    def graphMonthExchangeRateAsPoints(self, type = DataSetElement.AVERAGE):
        y_values = list()
        if type == DataSetElement.AVERAGE:
            y_values = [val*100.0 for val in self.getMonthAvgValues()]
        elif type == DataSetElement.BEGIN:
            y_values = [val*100.0 for val in self.getMonthBeginValues()]
        else:
            y_values = [val*100.0 for val in self.getMonthEndValues()]
        newGraph = Graph2D(list(range(1, len(y_values) + 1)), y_values, 'INR to USD Exchange Rates in ' + str(self.year), "Month", 'One Rupee In Dollars(cents)')
        newGraph.scatterPlot()

    def graphMonthExchangeRateAsLines(self, type = DataSetElement.AVERAGE):
        y_values = list()
        if type == DataSetElement.AVERAGE:
            y_values = [val*100.0 for val in self.getMonthAvgValues()]
        elif type == DataSetElement.BEGIN:
            y_values = [val*100.0 for val in self.getMonthBeginValues()]
        else:
            y_values = [val*100.0 for val in self.getMonthEndValues()]
        newGraph = Graph2D(list(range(1, len(y_values) + 1)), y_values, 'INR to USD Exchange Rates in ' + str(self.year), "Month", 'One Rupee In Dollars(cents)')
        newGraph.lineGraph()

    def graphDaysInMonthExchangeRatesAsPoints(self, month, type = DataSetElement.AVERAGE):
        monthRatesByDay = [self.rates[month][day]*100.0 for day in self.rates[month]]
        newGraph = Graph2D(list(range(len(self.rates[month]))), monthRatesByDay, 'INR to USD Exchange Rates in ' + str(month) + ' ' + str(self.year), 'Day', 'One Rupee In Dollars(cents)')
        newGraph.scatterPlot()

    def graphDaysInMonthExchangeRatesAsLines(self, month, type = DataSetElement.AVERAGE):
        monthRatesByDay = [self.rates[month][day]*100.0 for day in self.rates[month]]
        newGraph = Graph2D(list(range(len(self.rates[month]))), monthRatesByDay, 'INR to USD Exchange Rates in ' + str(month) + ' ' + str(self.year), 'Day', 'One Rupee In Dollars(cents)')
        newGraph.lineGraph()
