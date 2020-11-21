import backtrader
import pandas


class Minervini(backtrader.Strategy):

    def __init__(self):
        self.sample = len(self.data.array)
        self.uptrend = False

        if self.sample >= 50:
            self.sma50 = backtrader.indicators.SMA(period=50)
        if self.sample >= 150:
            self.sma150 = backtrader.ind.SMA(period=150)
        if self.sample >= 200:
            self.sma200 = backtrader.ind.SMA(period=200)

    def next(self):
        if self.sma50 > self.sma150 and self.sma150[0] > self.sma200[0] and not self.uptrend:
            if self.datas[0].close[0] > self.sma50:
                self.buy()
                self.uptrend = True
                print(self.datas[0].datetime.date(0))

        if self.sma200[0] > self.sma150[0] and self.uptrend:
            self.sell()
            self.uptrend = False


if __name__ == '__main__':
    cerebro = backtrader.Cerebro()
    dataframe = pandas.read_csv("stocks/ACEN.csv", header=0, parse_dates=["CHART_DATE"])
    cerebro.addstrategy(Minervini)

    data = backtrader.feeds.PandasData(dataname=dataframe, datetime=3, open=0, volume=1, close=2, high=4, low=5)
    cerebro.adddata(data)

    cerebro.run()
    cerebro.plot(style="bar")
