import os
from time import time

import backtrader
import pandas
from tqdm import tqdm


class Minervini(backtrader.Strategy):
    params = (
        ("output", {}),
        ("stock", ""),
    )

    def __init__(self):
        self.sample = len(self.data.array)
        self.uptrend = False

        self.params.output[self.params.stock] = []
        self.out = self.params.output[self.params.stock]

        if self.sample >= 50:
            self.sma50 = backtrader.indicators.SMA(period=50)
        else:
            self.sma50 = 0
        if self.sample >= 150:
            self.sma150 = backtrader.ind.SMA(period=150)
        else:
            self.sma150 = 0
        if self.sample >= 200:
            self.sma200 = backtrader.ind.SMA(period=200)
        else:
            self.sma200 = 0

    def next(self):
        if self.sma50 > self.sma150 > self.sma200 and not self.uptrend:
            if self.datas[0].close[0] > self.sma50 and self.datas[0].volume[0] > 5000000:
                self.buy()
                self.uptrend = True

                self.out.append(self.datas[0].datetime.date(0))

        if self.sma200 > self.sma150 and self.uptrend:
            self.sell()
            self.uptrend = False


if __name__ == '__main__':
    t = time()
    stocks = os.listdir("stocks")
    output = {}
    for stock in tqdm(stocks):
        name = stock.split(".")[0]
        cerebro = backtrader.Cerebro()
        cerebro.addstrategy(Minervini, output=output, stock=name)
        try:
            dataframe = pandas.read_csv("stocks/" + stock, header=0, parse_dates=["CHART_DATE"])
        except pandas.errors.EmptyDataError:
            continue

        data = backtrader.feeds.PandasData(dataname=dataframe, datetime=3, open=0, volume=1, close=2, high=4, low=5)
        cerebro.adddata(data)

        cerebro.run()
        # cerebro.plot(style="bar")

    print(output)
    print("Total stocks", len(output))
    print(int((time() - t) * 1000), "ms")
