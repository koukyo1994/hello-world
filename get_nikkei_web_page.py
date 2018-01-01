import urllib
from bs4 import BeautifulSoup

url = "http://www.nikkei.com/"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

title_tag = soup.title
title = title_tag.string

print(title_tag)
print(title)

stock_url = "http://www.nikkei.com/markets/kabu"
stock_html = urllib.request.urlopen(stock_url)
stock_soup = BeautifulSoup(stock_html, "html.parser")

print(stock_soup.title.string)

span = stock_soup.find_all("span")

nikkei_heikin = ""
for tag in span:
    try:
        string_ = tag.get("class").pop(0)
        if string_ in "mkc-stock_prices":
            nikkei_heikin = tag.string
            break
    except:
        pass

print(nikkei_heikin)