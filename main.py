import json
from argparse import ArgumentParser
from pathlib import Path

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.common import enums, errors
from src.domain import discount, signin, webdriver
from src.utils import logger


def main(headless: int, log_level: int, info_path: Path):
    log_level_list = [0, 10, 20, 30, 40, 50]
    if log_level not in log_level_list:
        ERROR_MSG = enums.LogMsg.LOG_LEVEL % log_level_list
        logger.critical(ERROR_MSG)
        raise AssertionError(ERROR_MSG)
    logger.setLevel(log_level)

    logger.info(enums.LogMsg.START)

    # declaring var
    with open(info_path, encoding="utf-8") as f:
        config: dict = json.load(f)

    # loading webdriver
    try:
        driver = webdriver.loading_webdriver(headless=headless)
    except Exception as e:
        ERROR_MSG = f"{webdriver.WebDriverState.ERROR}\n{e}"
        logger.exception(ERROR_MSG)
        raise Exception
    logger.info(webdriver.WebDriverState.SUCCESS)

    # web page loading
    try:
        driver.get(config["url"])
    except Exception:
        logger.error(webdriver.UrlState.ERROR)
        raise Exception
    logger.info(webdriver.UrlState.SUCCESS % driver.current_url)

    # login
    driver = signin.login(driver=driver, auth=config["auth"])
    try:
        login_res = signin.login_check(driver)
    except NoSuchElementException:
        logger.info(signin.LoginState.SUCCESS % driver.current_url)
    else:
        logger.error(signin.LoginState.ERROR % login_res)
        raise errors.LoginError

    # search car
    try:
        driver = discount.search_car(driver=driver, car_num=config["car_num"])
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except TimeoutException:
        logger.info(webdriver.SearchCarState.SUCCESS)
    else:
        logger.error(webdriver.SearchCarState.ERROR % alert.text)
        raise Exception

    # select car
    try:
        driver = discount.select_car(driver=driver, car_num=config["car_num"])
    except NoSuchElementException:
        logger.error(webdriver.SelectCarState.ERROR)
        raise Exception
    logger.info(webdriver.SelectCarState.SUCCESS)

    # discount parking 1h
    dc_type = discount.DiscountType.H1
    try:
        driver = discount.grant_discount(driver=driver, dc_type=dc_type)
    except NoSuchElementException as e:
        ERROR_MSG = f"{webdriver.DiscountResult.ERROR}\n{e}"
        logger.exception(ERROR_MSG)
        raise Exception
    logger.info(webdriver.DiscountResult.SUCCESS % dc_type.value[1])

    # refresh
    driver.refresh()
    logger.debug(enums.LogMsg.REFRESH)

    # search car
    try:
        driver = discount.search_car(driver=driver, car_num=config["car_num"])
        alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except TimeoutException:
        logger.info(webdriver.SearchCarState.SUCCESS)
    else:
        logger.error(webdriver.SearchCarState.ERROR % alert.text)
        raise Exception

    # select car
    try:
        driver = discount.select_car(driver=driver, car_num=config["car_num"])
    except NoSuchElementException:
        logger.error(webdriver.SelectCarState.ERROR)
    logger.info(webdriver.SelectCarState.SUCCESS)

    # discount parking 30m
    dc_type = discount.DiscountType.M30
    try:
        driver = discount.grant_discount(driver=driver, dc_type=dc_type)
    except NoSuchElementException as e:
        ERROR_MSG = f"{webdriver.DiscountResult.ERROR}\n{e}"
        logger.exception(ERROR_MSG)
        raise Exception
    logger.info(webdriver.DiscountResult.SUCCESS % dc_type.value[1])

    # quit web driver
    driver.quit()
    logger.info(enums.LogMsg.QUIT)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--headless", type=int, default=1)
    parser.add_argument("--log_level", type=int, default=20)
    parser.add_argument("--info_path", type=Path, default="info.json")
    args = vars(parser.parse_args())

    main(**args)
