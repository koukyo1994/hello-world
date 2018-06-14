import urllib
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time

time_flag = True

while time_flag:
    if datetime.now().second != 59:
        time.sleep(1)
        continue

    time.sleep(1)

    f = open("/home/hidehisa/hobby/scraper/data/nikkei_heikin.csv", "a")
    writer = csv.writer(f, lineterminator='\n')

    csv_list = []

    time_stamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    csv_list.append(time_stamp)

    url = "https://www.nikkei.com/markets/kabu/"
    html = urllib.request.urlopen(url)

    soup = BeautifulSoup(html, "html.parser")

    span = soup.find_all("span")
    nikkei_heikin = ""

    for tag in span:
        try:
            string_ = tag.get("class").pop(0)
            if "mkc-stock_prices" in string_:
                nikkei_heikin = tag.string

                break
        except:
            pass

    csv_list.append(nikkei_heikin)
    writer.writerow(csv_list)
    f.close()

    #if datetime.now().hour == 22:
    #    time_flag = False
