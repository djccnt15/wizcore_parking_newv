import os, sys,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import schedule

def job():
    # declaring var
    url = "http://220.75.173.245/"
    wiz_id = "A101101"
    wiz_pw = "Wizcore!0"
    car_num = "87로6770"

    # loading chrome web driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    driver.implicitly_wait(time_to_wait=5)

    # url loading
    try:
        driver.get(url)
        print(driver.current_url)
        print("get url success")
    except: print("get url error")

    # login
    try:
        driver.find_element_by_id("inputAccount").send_keys(wiz_id)
        driver.find_element_by_id("inputPassword").send_keys(wiz_pw)
        driver.find_element_by_class_name("btn.btn-lg.btn-primary.btn-block.btn-signin").click()
        print(driver.current_url)
        print("login success")
    except: print("login error")

    # search car
    search_box_car = driver.find_element_by_id("ip_car")
    search_box_car.send_keys(car_num)
    search_box_car.send_keys(Keys.RETURN)

    # select car
    try:
        driver.find_element_by_xpath('//*[@id="carsearch_table"]//tbody//tr//td[normalize-space()="%s"]' \
            % car_num).click()
        print("selecting car success")
    except: print("selecting car error")

    # discount parking
    try:
        driver.find_element_by_xpath('//*[@id="dc_items"]/label[3]/input').click()
        driver.find_element_by_id("DC_Active").click()
        driver.find_element_by_xpath('//*[@id="dc_items"]/label[2]/input').click()
        driver.find_element_by_id("DC_Active").click()
        print("discount success")
    except: print("discount error")

    # quit web driver
    driver.quit()
    print("web driver quit")

# schedule
schedule.every().friday.at("06:30").do(job)

# run every friday at 0630
while True:
    schedule.run_pending()
    time.sleep(1)
