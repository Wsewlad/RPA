# import selenium modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import system modules
import sys
from datetime import datetime
# import custom modules
from common.chrome_configs import chrome_options, chrome_service
import common.common_selenium_methods as common
import variables.constants as const
# import pages
from pages.home_page import HomePage
from pages.search_page import SearchPage

from RPA.Browser.Selenium import Selenium

# Exit
def exit(driver=None):
    if driver != None:
        driver.quit()
    sys.exit()

# search_phrase = "test"
# categories = ["category"]
# sections = ["section"]
# number_of_month = 1

browser_lib = Selenium()

def open_the_website(url):
    browser_lib.open_available_browser(url)


def search_for(term):
    input_field = "css:input"
    browser_lib.input_text(input_field, term)
    browser_lib.press_keys(input_field, "ENTER")


def store_screenshot(filename):
    browser_lib.screenshot(filename=filename)


# Define a main() function that calls the other functions in order:
def main():
    try:
        open_the_website("https://robocorp.com/docs/")
        search_for("python")
        store_screenshot("output/screenshot.png")
    finally:
        browser_lib.close_all_browsers()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()

# try:
    # driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    # # set window position
    # driver.set_window_position(*common.get_main_monitor_position())
    # driver.maximize_window()

    # # Home page
    # home_page = HomePage(driver)
    # home_page.lend_first_page()
    # home_page.enter_search_query("Ukraine")
    # # Search page
    # search_page = SearchPage(driver)
    # date_input_format = "%m/%d/%Y"
    # startDate = datetime.strptime("06/07/2023", date_input_format)
    # endDate = datetime.strptime("06/08/2023", date_input_format)
    # search_page.set_date_range(startDate, endDate)
    
    # search_page.expand_and_count_all_results()

# except Exception as e:
#     print("Error:", e)
# finally:
    # exit(driver)

