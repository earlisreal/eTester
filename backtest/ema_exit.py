from datetime import datetime

import backtrader
import pandas


class EMAExit(backtrader.Strategy):
    params = (
        ("entry", None),
        ("exits", {})
    )

    def __init__(self):
        self.entry = self.params.entry
        self.exits = self.params.exits

        self.indicators = {
            "ema5": backtrader.indicators.EMA(period=5),
            "ema10": backtrader.indicators.EMA(period=10),
            "ema20": backtrader.indicators.EMA(period=20),
            "sma10": backtrader.indicators.SMA(period=10),
            "sma20": backtrader.indicators.SMA(period=20),
            "sma50": backtrader.indicators.SMA(period=50),
        }

    def next(self):
        if self.datas[0].datetime.date(0) == self.entry:
            print("Buy Executed!")
            self.buy()

        for indicator in self.indicators.keys():
            if self.position and self.datas[0].close[0] < self.indicators[indicator][0]:
                if indicator not in self.exits:
                    self.exits[indicator] = {"date": self.datas[0].datetime.date(0), "price": self.datas[0].close[0]}


if __name__ == '__main__':
    while True:
        line = input()
        if len(line) < 1:
            break
        tokens = line.split("\t")

        entry = datetime.fromisoformat(tokens[1]).date()
        exits = {}

        cerebro = backtrader.Cerebro()
        cerebro.addstrategy(EMAExit, entry=entry, exits=exits)

        try:
            dataframe = pandas.read_csv("stocks/" + tokens[0] + ".csv", header=0, parse_dates=["CHART_DATE"])
        except pandas.errors.EmptyDataError:
            continue

        data = backtrader.feeds.PandasData(dataname=dataframe, datetime=3, open=0, volume=1, close=2, high=4, low=5)
        cerebro.adddata(data)

        cerebro.run()

        out = ""
        for value in exits.values():
            out += str(value["date"]) + "\t" + str(value["price"]) + "\t"
        print(out)

    print("bye")