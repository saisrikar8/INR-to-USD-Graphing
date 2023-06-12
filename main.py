from ExchangeRates import ExchangeRate

def main():
    rates = ExchangeRate(int(input('Enter the year(2010 to present inclusive): ')))
    rates.graphMonthExchangeRateAsLines()

if __name__ == '__main__':
    main()