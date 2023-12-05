import json
import platform
from argparse import ArgumentParser
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.common.enums import state
from src.utils.log import logger


def loading_webdriver(driver_path: Path | str, headless: int):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=str(driver_path), options=options)
    driver.implicitly_wait(time_to_wait=5)
    return driver


def login(driver: WebDriver, auth: dict):
    driver.find_element_by_id("inputAccount").send_keys(auth["id"])
    driver.find_element_by_id("inputPassword").send_keys(auth["pw"])
    driver.find_element_by_class_name(
        "btn.btn-lg.btn-primary.btn-block.btn-signin"
    ).click()
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
    try:
        driver.find_element_by_xpath(
            '//*[@id="dc_items"]/label[%s]/input' % (discount_type)
        ).click()
        driver.find_element_by_id("DC_Active").click()
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except Exception:
        if discount_type == 3:
            logger.info(state.DiscountResult.SUCCESS % "1h")
        elif discount_type == 2:
            logger.info(state.DiscountResult.SUCCESS % "30m")
        elif discount_type == 1:
            logger.info(state.DiscountResult.SUCCESS % "10m")
    else:
        try:
            raise Exception
        except Exception as e:
            ERROR_MSG = f"{e}\n{alert.text}"
            logger.exception(state.DiscountResult.ERROR % ERROR_MSG)
    return driver


def main(headless: int, log_level: int, info_path: Path):
    log_level_list = [0, 10, 20, 30, 40, 50]
    if log_level not in log_level_list:
        ERROR_MSG = state.LogMsg.LOG_LEVEL % log_level_list
        logger.critical(ERROR_MSG)
        raise AssertionError(ERROR_MSG)
    logger.setLevel(log_level)

    logger.info(state.LogMsg.START)

    # declaring var
    with open(info_path, encoding="utf-8") as f:
        info: dict = json.load(f)

    driver_path = "chromedriver"
    if platform.system() == "Windows":
        driver_path = f"{driver_path}.exe"

    # loading webdriver
    try:
        driver = loading_webdriver(driver_path=driver_path, headless=headless)
    except Exception as e:
        ERROR_MSG = f"{state.WebDriverState.ERROR}\n{e}"
        logger.exception(ERROR_MSG)
        raise Exception
    logger.info(state.WebDriverState.SUCCESS)

    # url loading
    try:
        driver.get(info["url"])
    except Exception:
        logger.error(state.UrlState.ERROR)
        raise Exception
    logger.info(state.UrlState.SUCCESS % driver.current_url)

    # login
    try:
        driver = login(driver=driver, auth=info["auth"])
    except Exception:
        logger.error(state.LoginState.ERROR)
        raise Exception
    logger.info(state.LoginState.SUCCESS % driver.current_url)

    # search car
    try:
        driver = search_car(driver=driver, car_num=info["car_num"])
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except Exception:
        logger.info(state.SearchCarState.SUCCESS)
    else:
        logger.error(state.SearchCarState.ERROR % alert.text)
        raise Exception

    # select car
    try:
        driver = select_car(driver=driver, car_num=info["car_num"])
    except Exception:
        logger.error(state.SelectCarState.ERROR)
        raise Exception
    logger.info(state.SelectCarState.SUCCESS)

    # discount parking 1h
    driver = discount(driver=driver, discount_type=3)

    # refresh
    driver.refresh()
    logger.debug(state.LogMsg.REFRESH)

    # search car
    try:
        driver = search_car(driver=driver, car_num=info["car_num"])
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except Exception:
        logger.info(state.SearchCarState.SUCCESS)
    else:
        logger.error(state.SearchCarState.ERROR % alert.text)
        raise Exception

    # select car
    try:
        driver = select_car(driver=driver, car_num=info["car_num"])
    except Exception:
        logger.error(state.SelectCarState.ERROR)
    logger.info(state.SelectCarState.SUCCESS)

    # discount parking 30m
    driver = discount(driver=driver, discount_type=2)

    # quit web driver
    driver.quit()
    logger.info(state.LogMsg.QUIT)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--headless", type=int, default=1)
    parser.add_argument("--log_level", type=int, default=20)
    parser.add_argument("--info_path", type=Path, default="info.json")
    args = vars(parser.parse_args())

    main(**args)
