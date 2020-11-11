import pandas
import requests
from tqdm import tqdm


def get_stock_data():
    print("Downloading Stock Historical Data")

    table = pandas.read_csv("stock_table.csv")
    for index, row in tqdm(table.iterrows()):
        body = {
            "cmpy_id": row["company_id"],
            "security_id": row["security_id"],
            "startDate": "01-01-2000",
            "endDate": "01-01-2030"
        }

        res = requests.post("https://edge.pse.com.ph/common/DisclosureCht.ax", json=body).json()

        data = res["chartData"]
        data_frame = pandas.DataFrame.from_dict(data)
        data_frame.to_csv("stocks/" + row["Stock Symbol"] + ".csv", index=False)


if __name__ == '__main__':
    get_stock_data()
    print("Done!")
