from selenium import webdriver

chrome_driver_path = "/Users/lenargasimov/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.python.org/")
# driver.find_element_by_id("pricelock-ourprice")
# # print(price.text)
# search_bar = driver.find_element_by_id("q")
# print(search_bar.get_attribute("placeholder"))

# logo = driver.find_element_by_class_name("python-logo")
# print(logo.size)

# documentation_link = driver.find_element_by_css_selector(".documentation-widget a")
# print(documentation_link.text)

event_times = driver.find_element_by_css_selector(".event-widget time")
for time in event_times:
    print(time.text)




# driver.close()
driver.quit()