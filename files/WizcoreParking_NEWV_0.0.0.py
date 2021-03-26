from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# declaring var
driver_loca = ".\chromedriver.exe"
url = "http://220.75.173.245/"
wiz_id = "A101101"
wiz_pw = "Wizcore!0"
car_num = "test_car_num"

# loading chrome web driver
driver = webdriver.Chrome(driver_loca)
driver.implicitly_wait(time_to_wait=5)

# url loading
driver.get(url)

# login
driver.find_element_by_id("inputAccount").send_keys(wiz_id)
driver.find_element_by_id("inputPassword").send_keys(wiz_pw)
driver.find_element_by_class_name("btn.btn-lg.btn-primary.btn-block.btn-signin").click()
driver.implicitly_wait(time_to_wait=5)

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

# quit driver
# driver.quit()

# table_search_result = driver.find_element_by_id("carsearch_table")
# tbody = table_search_result.find_element_by_tag_name("tbody")
# rows = tbody.find_elements_by_tag_name("tr")
# table_search_result
# for index, value in enumerate(rows):
#     body = value.find_elements_by_tag_name("td")[0]
#     print(body.text)
