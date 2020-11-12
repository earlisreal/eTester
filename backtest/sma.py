import backtrader
import pandas

if __name__ == '__main__':
    cerebro = backtrader.Cerebro()

    dataframe = pandas.read_csv("stocks/ACEN.csv", header=0, parse_dates=["CHART_DATE"])
    print(dataframe.head())
    data = backtrader.feeds.PandasData(dataname=dataframe, datetime=3, open=0, volume=1, close=2, high=4, low=5)
    cerebro.adddata(data)

    cerebro.run()

    cerebro.plot(style="bar")

