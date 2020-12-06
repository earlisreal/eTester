from datetime import datetime, timedelta

import backtrader
import pandas


class EMA_Exit(backtrader.Strategy):
    params = (
        ("entry", None),
        ("ema_period", 5)
    )

    def __init__(self):
        self.entry = self.params.entry
        self.ema = backtrader.indicators.SMA(period=self.params.ema_period)
        self.end = False

    def next(self):
        # print(self.datas[0].datetime.date(0))
        if self.datas[0].datetime.date(0) == self.entry:
            print("Buy Executed!")
            self.buy()

        print(self.datas[0].datetime.date(0), self.datas[0].close[0], self.ema[0])
        if self.position and self.datas[0].close[0] < self.ema:
            print("Sell Executed!")
            self.sell()
            self.end = True


if __name__ == '__main__':
    while True:
        line = input()
        if len(line) < 1:
            break
        tokens = line.split("\t")

        entry = datetime.fromisoformat(tokens[1]).date()

        cerebro = backtrader.Cerebro()
        cerebro.addstrategy(EMA_Exit, entry=entry)

        try:
            dataframe = pandas.read_csv("stocks/" + tokens[0] + ".csv", header=0, parse_dates=["CHART_DATE"])
        except pandas.errors.EmptyDataError:
            continue

        data = backtrader.feeds.PandasData(fromdate=entry - timedelta(days=10), todate=entry + timedelta(days=60), dataname=dataframe, datetime=3, open=0, volume=1, close=2, high=4, low=5)
        cerebro.adddata(data)

        cerebro.run()
        # TODO: Save all EMA price and date to dict then compute manually the percentage

    print("bye")