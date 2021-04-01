import os, sys,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import schedule

def job():
    # declaring var
    url = "http://220.75.173.245/"
    wiz_id = "****"
    wiz_pw = "****"
    car_num = "****"

    # loading chrome web driver
    if getattr(sys, 'frozen', False):
        chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
        driver = webdriver.Chrome(chromedriver_path)
    else:
        driver = webdriver.Chrome()

    driver.implicitly_wait(time_to_wait=5)

    # url loading
    driver.get(url)

    # login
    driver.find_element_by_id("inputAccount").send_keys(wiz_id)
    driver.find_element_by_id("inputPassword").send_keys(wiz_pw)
    driver.find_element_by_class_name("btn.btn-lg.btn-primary.btn-block.btn-signin").click()

    # search car
    search_box_car = driver.find_element_by_id("ip_car")
    search_box_car.send_keys(car_num)
    search_box_car.send_keys(Keys.RETURN)

    # select car
    driver.find_element_by_xpath('//*[@id="carsearch_table"]//tbody//tr//td[normalize-space()="%s"]' % car_num).click()

    # discount parking
    driver.find_element_by_xpath('//*[@id="dc_items"]/label[3]/input').click()
    driver.find_element_by_id("DC_Active").click()
    driver.find_element_by_xpath('//*[@id="dc_items"]/label[2]/input').click()
    driver.find_element_by_id("DC_Active").click()

    # quit web driver
    driver.quit()

# schedule
schedule.every().friday.at("06:30").do(job)

# run every friday at 0630
while True:
    schedule.run_pending()
    time.sleep(1)
