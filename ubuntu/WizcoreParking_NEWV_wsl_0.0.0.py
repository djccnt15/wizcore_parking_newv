import os, sys, time, schedule
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# declaring var
url = "http://220.75.173.245/"
wiz_id = "A101101"
wiz_pw = "Wizcore!0"
car_num = "87로6770"

def job():
    # loading chrome web driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    driver.implicitly_wait(time_to_wait=5)

    # url loading
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try: driver.get(url)
    except: print("%s: get url error" %(current_time), flush=True)
    else: print("%s: get url success, current url is %s" %(current_time, driver.current_url), flush=True)

    # login
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        driver.find_element_by_id("inputAccount").send_keys(wiz_id)
        driver.find_element_by_id("inputPassword").send_keys(wiz_pw)
        driver.find_element_by_class_name("btn.btn-lg.btn-primary.btn-block.btn-signin").click()
    except: print("%s: login error" %(current_time), flush=True)
    else: print("%s: login success, current url is %s" %(current_time, driver.current_url), flush=True)

    # search car
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    search_box_car = driver.find_element_by_id("ip_car")
    search_box_car.send_keys(car_num)
    search_box_car.send_keys(Keys.RETURN)
    wait = WebDriverWait(driver, 1)
    try: alert = wait.until(EC.alert_is_present())
    except: print("%s: search car success" %(current_time), flush=True)
    else:
        print("%s error message: %s" %(current_time, alert.text), flush=True)
        alert.dismiss()

    # select car
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        driver.find_element_by_xpath('//*[@id="carsearch_table"]//tbody//tr//td[normalize-space()="%s"]' \
            %(car_num)).click()
    except: print("%s: selecting car error" %(current_time), flush=True)
    else: print("%s: selecting car success" %(current_time), flush=True)

    # discount parking
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        driver.find_element_by_xpath('//*[@id="dc_items"]/label[3]/input').click()
        driver.find_element_by_id("DC_Active").click()
        driver.find_element_by_xpath('//*[@id="dc_items"]/label[2]/input').click()
        driver.find_element_by_id("DC_Active").click()
    except: print("%s: discount error" %(current_time), flush=True)
    else: print("%s: discount success" %(current_time), flush=True)

    # quit web driver
    driver.quit()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("%s: web driver quit" %(current_time), flush=True)

# schedule
schedule.every().friday.at("06:30").do(job)

# run every friday at 0630
while True:
    schedule.run_pending()
    time.sleep(1)
