# Indian Rupee value in US Dollar

This code will prompt you for a year from 2010 and outputs a graph of the Indian Rupee's value in US Dollars throughout that year. This program extracts data from <a href = "https://www.exchangerates.org.uk/INR-USD-spot-exchange-rates-history-2010.html">this website</a>. This is a great website as it not only includes exchange rates values from 2010, but every year after it too. The even better part is that it has the rate for everyday of each year!

## How the program works

This isn't a complex program. I only needed to create two classes and an enum(just to make my code shorter). Here is a breakdown of the steps before we go into a little more detail:

1. An object of class `ExchangeRate` is created with the inputted parameter of the year.
2. The `ExchangeRate.graphMonthExchangeRateAsLines()` method is called.
3. A `list` of exchange rates for each month is generated using some helper methods in the `ExchangeRate` class.
4. An object of class `Graph2D` is created.
5. The `Graph2D.lineGraph()` method is called and a graph is generated.

First, the user is prompted for the year that they want the exchange rate graph's data to be about. Then the constructor method of the `ExchangeRate` class is called. Here is the line of code that writes takes the input and calls the class's `__init__` method.

```python
    rates = ExchangeRate(int(input('Enter the year(2010 to present inclusive): ')))
```

An object of type `ExchangeRate` is created. The following `python` code snippet shows the `__init__` method of the class.

```python
class ExchangeRate:
    year = int()
    rates = dict()

    def __init__(self, year):
        self.year = year
        self.rates = self.getExchangeRatesByDay(year)
```

The year inputted by the user is one of the parameters of the `__init__` method as it allows the class to generate graphs of different years and add more variability to the output. Then, the `getExchangeRatesByDay()` method is called. Here is the code for the method.

```python
def getExchangeRatesByDay(self, newYear):
        url = 'https://www.exchangerates.org.uk/INR-USD-spot-exchange-rates-history-' + str(newYear) + '.html'
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
```

The function implements the `urllib` library that is built-in to Python. It also uses the `BeautifulSoup` library to extract the data from the url. This data is then placed into a Python dictionary, which is similar to JSON if you aren't familiar with Python. Each key is each month of the year. The value of each key is another dictionary where the key represents the day of the month. The value of these inner dictionaries represent the value of one Rupee in dollars as a `float` value. This dictionary is like a calendar. When this function is done, the `ExchangeRate` object will be created.

Next, the `graphMonthExchangeRateAsLines()` method from the `ExchangeRate` class is called. The method has one optional parameter. Here is the code for the method:

```python
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
```

This method first generates a `list` of values in cents. The optional parameter is an enum that has three options. Here is the definition of the enum.

```python
from enum import Enum

class DataSetElement(Enum):
    BEGIN = 1
    AVERAGE = 2
    END = 3
```

The method's output varies based on the parameter inputted. The output of the method is a `list` of the value of the Rupee each month. Each setting of the parameter changes the value of each month's Rupee value. It can either be the value at the end of each month, at the beginning of each month, or the average value of each month. The default is the average value.

Then, based on the parameter, a different function is called to generate the list. Here is the code that generates the list.

```python
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
```

Each method starts out the same. The `for` loop iterates through the dictionary generated by the `getExchangeRatesByDay()` method.  The `getMonthAvgValues()` method iterates throught the inner dictionaries that hold the Rupee's value for each day. Then, it takes the sum of all the values and divides it by the number of days in the month, which will result in the average. Each average is appended to a list and is returned in the order of the months. The `getMonthEndValues()` takes the last day's Rupee value and `getMonthStartValues()` takes the first day's Rupee value. Each value is then appended to the list. Then, that list is returned.

Next, an object of type `Graph2D` is created. Here is the `__init__` method for the `Graph2d` class:

```python
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
```

The method stores inputted parameters and sets the graph's title and labels the x and y axes. 

The last step of the `graphMonthExchangeRateAsLines()` is calling the `lineGraph()` method. Since all the graph's properties are defined in the constructor method, the method will implement the `plot()` method of the `matplotlib` library to construct the graph. Here is the code for the `lineGraph()` method:

```python
def lineGraph(self):
        graph.plot(self.x_values, self.y_values, c = 'r')
        graph.show()
```

You can now run the code and try out different values for yourself. However, before you start, make sure to run the following commands in your command line:

If you already have `pip` installed, you can skip the first step.

1. `pip install pip`

2. `pip install matplotlib`

3. `pip install bs4`

Now that you have downloaded all the required packages, you can start playing around with the code. There are also other methods that allow you to graph the data in different ways.

Let's run the code first:

<figure>
    <img src = "./Screenshot 2023-06-12 230522.png" alt = "Figure 1">
    <figcaption>The picture above shows the input prompt for the year of the exchange rate data. Let's enter 2021.</figcaption>
</figure>

<figure>
    <img src = "./Figure_1.png" alt = "Figure 2">
    <figcaption>The picture above shows the resulting output graph.</figcaption>
</figure>

## Other Methods

A majority of the methods in the `ExchangeRate` and `Graph2D` classes have been used in the program. However, there are still some methods which can be very useful as well. This section will allow you to understand how to use those methods, so you can use them yourself.

### ExchangeRate Class Methods

First, let's cover the methods in the `ExchangeRate` class. These methods will alter the data or how the graph looks.

#### graphMonthExchangeRateAsPoints()

This method is similar to the `graphMonthExchangeRateAsLines()` method because it generates the exact same data. However, the one difference is that the graph is composed a little differently from the `graphMonthExchangeRateAsLines()` method. This is because the method outputs a scatter plot rather than a line graph. You will gain a better understanding about how the graph is produce in [the `Graph2D` section](#graph2dmethods). Here is the code for the `graphMonthExchangeRateAsPoints()` method:

```python
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
```

#### graphDaysInMonthExchangeRatesAsLines()

This method is also similar to the `graphMonthExchangeRateAsLines()` method. In this case, a line graph is created, but this method takes the exchange rate of everyday in an individual month rather looking at a whole year. The `graphDaysInMonthExchangeRatesAsLines()` method takes the parameter of the month that you want the graph to be about. The code below shows the definition of this method.

```python
def graphDaysInMonthExchangeRatesAsLines(self, month):
        monthRatesByDay = [self.rates[month][day]*100.0 for day in self.rates[month]]
        newGraph = Graph2D(list(range(len(self.rates[month]))), monthRatesByDay, 'INR to USD Exchange Rates in ' + str(month) + ' ' + str(self.year), 'Day', 'One Rupee In Dollars(cents)')
        newGraph.lineGraph()
```

#### graphDaysInMonthExchangeRatesAsPoints()

The `graphDaysInMonthExchangeRatesAsPoints()` method takes the data of one individual month and graphs it as a scatter plot. The parameter of this method is the month that the data should be about.

```python
def graphDaysInMonthExchangeRatesAsLines(self, month):
        monthRatesByDay = [self.rates[month][day]*100.0 for day in self.rates[month]]
        newGraph = Graph2D(list(range(len(self.rates[month]))), monthRatesByDay, 'INR to USD Exchange Rates in ' + str(month) + ' ' + str(self.year), 'Day', 'One Rupee In Dollars(cents)')
        newGraph.lineGraph()
```

<h3 id = "graph2dmethods">Graph2D Class Methods</h3>

There is only one more method that hasn't been covered for the `Graph2D` methods.

#### scatterPlot()

In the previous section, we explored the methods of the `ExchangeRate` class. A lot of those methods change how the graph is portrayed. As mentioned earlier, the `graphMonthExchangeRateAsLines()` method uses the `lineGraph()` method of the `ExchangeRate` class to produce a line graph. The `graphMonthExchangeRateAsPoints()` produces a scatter plot with all the data being placed on the graph as points. The `scatterPlot()` method of the `Graph2D` class was implemented in the `graphMonthExchangeRateAsPoints()` method. This method implements the `scatter()` method of the `matplotlib` library to create a graph. Here is the code for this method:

```python
def scatterPlot(self):
        graph.scatter(self.x_values, self.y_values, marker = 'x', c = 'r')
        graph.show()
```
