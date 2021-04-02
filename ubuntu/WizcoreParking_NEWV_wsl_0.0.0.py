import os, sys, time, schedule, urllib3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("%s: code starts running" %(start_time), flush=True)
del start_time

# declaring var
url = "http://220.75.173.245/"
wiz_id = "****"
wiz_pw = "****"
car_num = "****"

def loading_webdriver():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        global driver
        driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        driver.implicitly_wait(time_to_wait=5)
    except: print("%s: loading webdriver error" %(current_time), flush=True)
    else: print("%s: loading webdriver success" %(current_time), flush=True)

def search_car():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    search_box_car = driver.find_element_by_id("ip_car")
    search_box_car.send_keys(car_num)
    search_box_car.send_keys(Keys.RETURN)
    try: alert = WebDriverWait(driver, timeout=2).until(EC.alert_is_present())
    except: print("%s: search car success" %(current_time), flush=True)
    else:
        print("%s error message: %s" %(current_time, alert.text), flush=True)
        alert.dismiss()

def select_car():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        driver.find_element_by_xpath('//*[@id="carsearch_table"]//tbody//tr//td[normalize-space()="%s"]' %(car_num)).click()
    except: print("%s: selecting car error" %(current_time), flush=True)
    else: print("%s: selecting car success" %(current_time), flush=True)

def discount(discount_type):
    # discount type: 1 == 10min, 2 == 30min, 3 == 1hour
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        driver.find_element_by_xpath('//*[@id="dc_items"]/label[%s]/input' %(discount_type)).click()
        driver.find_element_by_id("DC_Active").click()
    except: print("%s: discount error" %(current_time), flush=True)
    else:
        if discount_type == 3: print("%s: 1 hour discount success" %(current_time), flush=True)
        elif discount_type == 2: print("%s: 30 minute discount success" %(current_time), flush=True)
        elif discount_type == 1: print("%s: 10 minute discount success" %(current_time), flush=True)

def job():
    # loading webdriver
    loading_webdriver()

    # url connection check
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    if response.status == 200:
        print("%s: current http status code is %s, connection OK" %(current_time, response.status), flush=True)

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

        # search car and select car
        search_car()
        select_car()

        # discount parking 1h
        discount(3)

        # refresh
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        driver.refresh()
        print("%s: refresh page" %(current_time), flush=True)

        # search car and select car
        search_car()
        select_car()

        # discount parking 30m
        discount(2)

        # quit web driver
        driver.quit()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("%s: web driver quit" %(current_time), flush=True)
    else: print("%s: current http status code is %s, http has a problem" %(current_time, response.status), flush=True)

# schedule
schedule.every().friday.at("06:30").do(job)

# run every friday at 0630
while True:
    schedule.run_pending()
    time.sleep(1)
