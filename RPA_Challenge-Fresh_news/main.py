# import selenium modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import system modules
import sys
from datetime import datetime
# import custom modules
from Common.chrome_configs import chrome_options, chrome_service
# import pages
from Pages.home_page import HomePage
from Pages.search_page import SearchPage

# Exit
def exit(driver=None):
    if driver != None:
        driver.quit()
    sys.exit()

# search_phrase = "test"
# categories = ["category"]
# sections = ["section"]
# number_of_month = 1

try:
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    driver.get("https://www.nytimes.com")

    home_page = HomePage(driver)
    home_page.enter_search_query("Ukraine")

    search_page = SearchPage(driver)
    date_input_format = "%m/%d/%Y"
    startDate = datetime.strptime("06/07/2023", date_input_format)
    endDate = datetime.strptime("06/08/2023", date_input_format)
    search_page.set_date_range(startDate, endDate)
    
    search_page.expand_and_count_all_results()

except Exception as e:
    print("Error:", e)
# finally:
    # exit(driver)

