import json
from argparse import ArgumentParser
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.common.enums import state
from src.common.error import LoginError
from src.utils.log import logger


def loading_webdriver(headless: int):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(time_to_wait=5)
    return driver


def login(driver: WebDriver, auth: dict):
    driver.find_element(by=By.ID, value="inputAccount").send_keys(auth["id"])
    driver.find_element(by=By.ID, value="inputPassword").send_keys(auth["pw"])
    driver.find_element(
        by=By.CLASS_NAME, value="btn.btn-lg.btn-primary.btn-block.btn-signin"
    ).click()
    return driver


def login_check(driver: WebDriver):
    profile_name_card = driver.find_element(by=By.ID, value="profile-name")
    if profile_name_card:
        return profile_name_card.text


def search_car(driver: WebDriver, car_num):
    search_box_car = driver.find_element(by=By.ID, value="ip_car")
    search_box_car.send_keys(car_num)
    search_box_car.send_keys(Keys.RETURN)
    return driver


def select_car(driver: WebDriver, car_num: str):
    driver.find_element(
        by=By.XPATH,
        value=f'//*[@id="carsearch_table"]//tbody//tr//td[normalize-space()="{car_num}"]',
    ).click()
    return driver


def discount(driver: WebDriver, discount_type: int):
    """discount type: 1 == 10min, 2 == 30min, 3 == 1hour"""
    try:
        driver.find_element(
            by=By.XPATH, value=f'//*[@id="dc_items"]/label[{discount_type}]/input'
        ).click()
        driver.find_element(by=By.ID, value="DC_Active").click()
    except NoSuchElementException as e:
        ERROR_MSG = f"{state.DiscountResult.ERROR}\n{e}"
        logger.exception(ERROR_MSG)
        raise NoSuchElementException

    if discount_type == 3:
        logger.info(state.DiscountResult.SUCCESS % "1h")
    elif discount_type == 2:
        logger.info(state.DiscountResult.SUCCESS % "30m")
    elif discount_type == 1:
        logger.info(state.DiscountResult.SUCCESS % "10m")

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
        config: dict = json.load(f)

    # loading webdriver
    try:
        driver = loading_webdriver(headless=headless)
    except Exception as e:
        ERROR_MSG = f"{state.WebDriverState.ERROR}\n{e}"
        logger.exception(ERROR_MSG)
        raise Exception
    logger.info(state.WebDriverState.SUCCESS)

    # web page loading
    try:
        driver.get(config["url"])
    except Exception:
        logger.error(state.UrlState.ERROR)
        raise Exception
    logger.info(state.UrlState.SUCCESS % driver.current_url)

    # login
    driver = login(driver=driver, auth=config["auth"])
    try:
        login_res = login_check(driver)
    except NoSuchElementException:
        logger.info(state.LoginState.SUCCESS % driver.current_url)
    else:
        logger.error(state.LoginState.ERROR % login_res)
        raise LoginError

    # search car
    try:
        driver = search_car(driver=driver, car_num=config["car_num"])
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except TimeoutException:
        logger.info(state.SearchCarState.SUCCESS)
    else:
        logger.error(state.SearchCarState.ERROR % alert.text)
        raise Exception

    # select car
    try:
        driver = select_car(driver=driver, car_num=config["car_num"])
    except NoSuchElementException:
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
        driver = search_car(driver=driver, car_num=config["car_num"])
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except TimeoutException:
        logger.info(state.SearchCarState.SUCCESS)
    else:
        logger.error(state.SearchCarState.ERROR % alert.text)
        raise Exception

    # select car
    try:
        driver = select_car(driver=driver, car_num=config["car_num"])
    except NoSuchElementException:
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
