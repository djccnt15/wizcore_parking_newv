from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


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
