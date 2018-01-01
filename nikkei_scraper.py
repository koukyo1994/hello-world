import urllib
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time

time_flag = True

while time_flag:
    if datetime.now().minute != 59:
        time.sleep(58)
        continue

    with open("data/nikkei_heikin.csv", "a") as f:
        writer = csv.writer(f, lineterminator='\n')

        while datetime.now().second != 59:
            time.sleep(1)

        time.sleep(1)
        csv_list = []

        time_stamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        csv_list.append(time_stamp)

        url = "http://www.nikkei.com/market/kabu"
        html = urllib.request.urlopen(url)

        soup = BeautifulSoup(html, "html.parser")

        span = soup.find_all("span")
        nikkei_heikin = ""

        for tag in span:
            try:
                string_ = tag.get("class").pop(0)
                if string_ in "mkc-stock_price":
                    nikkei_heikin = tag.string

                    break
            except:
                pass

        print(time_stamp, nikkei_heikin)
        csv_list.append(nikkei_heikin)
        writer.writerow(csv_list)

    if datetime.now().hour == 23:
        time_flag = False
