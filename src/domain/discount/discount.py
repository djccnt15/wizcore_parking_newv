from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from .enum.discount_enum import DiscountType


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


def grant_discount(driver: WebDriver, dc_type: DiscountType):
    driver.find_element(
        by=By.XPATH, value=f'//*[@id="dc_items"]/label[{dc_type.value[0]}]/input'
    ).click()
    driver.find_element(by=By.ID, value="DC_Active").click()
    return driver
