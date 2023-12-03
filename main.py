import json
import platform
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def loading_webdriver(driver_path: Path | str, headless: int):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=str(driver_path), options=options)
    driver.implicitly_wait(time_to_wait=5)
    return driver


def search_car(driver: WebDriver, car_num):
    search_box_car = driver.find_element_by_id("ip_car")
    search_box_car.send_keys(car_num)
    search_box_car.send_keys(Keys.RETURN)
    return driver


def select_car(driver: WebDriver, car_num: str):
    driver.find_element_by_xpath(
        '//*[@id="carsearch_table"]//tbody//tr//td[normalize-space()="%s"]' % (car_num)
    ).click()
    return driver


def discount(driver: WebDriver, discount_type: int):
    """discount type: 1 == 10min, 2 == 30min, 3 == 1hour"""
    current_time = datetime.now().replace(microsecond=0)
    try:
        driver.find_element_by_xpath(
            '//*[@id="dc_items"]/label[%s]/input' % (discount_type)
        ).click()
        driver.find_element_by_id("DC_Active").click()
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except Exception:
        if discount_type == 3:
            print("%s: 1 hour discount success" % (current_time))
        elif discount_type == 2:
            print("%s: 30 minute discount success" % (current_time))
        elif discount_type == 1:
            print("%s: 10 minute discount success" % (current_time))
    else:
        print("%s: discount error, %s" % (current_time, alert.text))
        alert.dismiss()
    return driver


def main(headless: int):
    start_time = datetime.now().replace(microsecond=0)
    print("%s: code starts running" % (start_time))

    # declaring var
    url = "http://220.75.173.245/"

    with open("auth.json", encoding="utf-8") as input_json:
        auth = json.load(input_json)

    driver_path = "chromedriver"
    if platform.system() == "Windows":
        driver_path = "chromedriver.exe"

    # loading webdriver
    current_time = datetime.now().replace(microsecond=0)
    try:
        driver = loading_webdriver(driver_path=driver_path, headless=headless)
    except Exception:
        print("%s: loading webdriver error" % (current_time))
        raise Exception
    else:
        print("%s: loading webdriver success" % (current_time))

    # url loading
    current_time = datetime.now().replace(microsecond=0)
    try:
        driver.get(url)
    except Exception:
        print("%s: get url error" % (current_time))
        raise Exception
    else:
        print(
            "%s: get url success, current url is %s"
            % (current_time, driver.current_url),
            flush=True,
        )

    # login
    current_time = datetime.now().replace(microsecond=0)
    try:
        driver.find_element_by_id("inputAccount").send_keys(auth["wiz_id"])
        driver.find_element_by_id("inputPassword").send_keys(auth["wiz_pw"])
        driver.find_element_by_class_name(
            "btn.btn-lg.btn-primary.btn-block.btn-signin"
        ).click()
    except Exception:
        print("%s: login error" % (current_time))
        raise Exception
    else:
        print(
            "%s: login success, current url is %s" % (current_time, driver.current_url),
            flush=True,
        )

    # search car
    current_time = datetime.now().replace(microsecond=0)
    driver = search_car(driver=driver, car_num=auth["car_num"])
    try:
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except Exception:
        print("%s: search car success" % (current_time))
        raise Exception
    else:
        print("%s: search car error, %s" % (current_time, alert.text))
        alert.dismiss()

    # select car
    current_time = datetime.now().replace(microsecond=0)
    try:
        select_car(driver=driver, car_num=auth["car_num"])
    except Exception:
        print("%s: selecting car error" % (current_time))
        raise Exception
    else:
        print("%s: selecting car success" % (current_time))

    # discount parking 1h
    driver = discount(driver=driver, discount_type=3)

    # refresh
    current_time = datetime.now().replace(microsecond=0)
    driver.refresh()
    print("%s: refresh page" % (current_time))

    # search car
    current_time = datetime.now().replace(microsecond=0)
    driver = search_car(driver=driver, car_num=auth["car_num"])
    try:
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except Exception:
        print("%s: search car success" % (current_time))
    else:
        print("%s: search car error, %s" % (current_time, alert.text))
        alert.dismiss()

    # select car
    current_time = datetime.now().replace(microsecond=0)
    try:
        select_car(driver=driver, car_num=auth["car_num"])
    except Exception:
        print("%s: selecting car error" % (current_time))
    else:
        print("%s: selecting car success" % (current_time))

    # discount parking 30m
    driver = discount(driver=driver, discount_type=2)

    # quit web driver
    driver.quit()
    current_time = datetime.now().replace(microsecond=0)
    print("%s: web driver quit" % (current_time))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--headless", type=int)
    args = vars(parser)

    main(**args)
