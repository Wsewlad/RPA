# import RPA modules
from RPA.Browser.Selenium import Selenium
# import system modules
from datetime import datetime
# import pages
from pages.home_page import HomePage
from pages.search_page import SearchPage

# search_phrase = "test"
# categories = ["category"]
# sections = ["section"]
# number_of_month = 1


def main():
    try:
        browser_lib: Selenium = Selenium()
        browser_lib.auto_close = False

        # Home page
        home_page = HomePage(browser_lib)
        home_page.lend_first_page()
        home_page.enter_search_query("Ukraine")
        # Search page
        search_page = SearchPage(browser_lib)
        date_input_format = "%m/%d/%Y"
        startDate = datetime.strptime("06/07/2023", date_input_format)
        endDate = datetime.strptime("06/08/2023", date_input_format)
        search_page.set_date_range(startDate, endDate)

        search_page.expand_and_count_all_results()

    except Exception as e:
        print("Error:", e)
    finally:
        print("End")
        # browser_lib.close_all_browsers()


if __name__ == "__main__":
    main()
