import os
import shutil
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from urllib.request import urlretrieve


def access():
    disp = Display(visible=0, size=(800, 600))
    disp.start()

    print("========================================")
    print("Start query")
    if os.name == "nt":
        driver_path = "../windows/chromedriver.exe"
    elif os.name == "posix":
        driver_path = "../linux/chromedriver"
    elif os.name == "darwin":
        driver_path = "../mac/chromedriver"

    driver = webdriver.Chrome(executable_path=driver_path)
    driver.implicitly_wait(10)
    driver.get("https://www.google.co.jp/imghp?hl=ja")
    return driver, disp


def dir_manage(tag, basecolor):
    file_path = f"../../data/{basecolor}/{tag}"
    if not os.path.isdir(f"../../data/{basecolor}"):
        os.mkdir(f"../../data/{basecolor}")
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)

    os.mkdir(file_path)
    print(f"Made directory {file_path}")
    return file_path


def get_tag(driver, query):
    input_query = driver.find_element_by_xpath('//*[@id="lst-ib"]')
    input_query.send_keys(query)
    input_query.send_keys(Keys.ENTER)

    tags = driver.find_elements_by_css_selector(".ZO5Spb")
    return tags, driver


def search_with_one_tag(driver, tag):
    tag.click()
    backtag = driver.find_element_by_css_selector(".jfZuRd")
    for i in range(5):
        driver.execute_script('scroll(0, document.body.scrollHeight)')
        print('Waiting for contents to be loaded...', file=sys.stderr)
        time.sleep(2)

    button = driver.find_element_by_xpath('//*[@id="smb"]')
    button.click()
    print("Waiting for contents to be loaded...", file=sys.stderr)
    time.sleep(2)

    for i in range(5):
        driver.execute_script('scroll(0, document.body.scrollHeight)')
        print('Waiting for contents to be loaded...', file=sys.stderr)
        time.sleep(2)
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    jscontroller = soup.find_all("div", attrs={"jscontroller": "Q7Rsec"})
    print(f"Found {len(jscontroller)} pictures.")
    print("===================================")
    backtag.click()
    return driver, jscontroller


def retreive_img(jscontroller, tag, basecolor):
    file_path = dir_manage(tag, basecolor)
    n = len(jscontroller)
    for i, js in enumerate(jscontroller):
        img = js.find_all("img")[0]
        src = img.get("data-src")
        try:
            urlretrieve(src, f"{file_path}/{i}.jpg")
            time.sleep(3)
            percentage = ((i+1) / n) * 100
            sys.stdout.write(f"\r Finished {percentage:.2f} percent")
            sys.stdout.flush()
        except Exception as e:
            try:
                src = img.get("src")
                urlretrieve(src, f"{file_path}/{i}.jpg")
                time.sleep(3)
                percentage = ((i+1) / n) * 100
                sys.stdout.write(f"\r Finished {percentage:.2f} percent")
                sys.stdout.flush()
            except Exception:
                print(f"Failed to retreive: {src}")


def img_query_with_one_tag(query):
    driver, disp = access()
    tags, driver = get_tag(driver, query)
    basecolor = query.split()[1]
    for tag in tags:
        tag_name = tag.find_element_by_tag_name("span").text
        driver, jscontroller = search_with_one_tag(driver, tag)
        retreive_img(jscontroller, tag_name, basecolor)
    driver.quit()
    disp.stop()


if __name__ == "__main__":
    colors = ["赤", "青", "緑", "黄色", "紫", "黒", "白", "オレンジ"]
    for c in colors:
        query = f"ワンピース {c}"
        img_query_with_one_tag(query)
