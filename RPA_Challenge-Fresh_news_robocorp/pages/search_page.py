# import RPA modules
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.support.wait import WebDriverWait
# import system modules
from urllib.parse import urlparse, parse_qs
# import custom modules


class SearchPage:
    SEARCH_DATE_DROPDOWN = 'css:[data-testid="search-date-dropdown-a"]'
    SPECIFIC_DATES_OPTION = 'css:[value="Specific Dates"]'
    START_DATE_FIELD = 'css:[data-testid="DateRange-startDate"]'
    END_DATE_FIELD = 'css:[data-testid="DateRange-endDate"]'
    SHOW_MORE_BUTTON = 'css:[data-testid="search-show-more-button"]'
    SEARCH_RESULTS_LIST = 'css:[data-testid="search-results"]'
    SEARCH_ITEM = 'css:[data-testid="search-bodega-result"]'

    date_input_format = "%m/%d/%Y"
    date_query_format = "%Y%m%d"

    def __init__(self, browser_lib):
        self.browser_lib = browser_lib
        title = self.browser_lib.get_title()
        assert title == "The New York Times - Search", "This is not Search Page, current page is - " + \
            self.browser_lib.get_location()

    # Set date range
    def set_date_range(self, startDate, endDate):
        try:
            # navigate to date range picker
            self.browser_lib.get_webElement(self.SEARCH_DATE_DROPDOWN).click()
            self.driver.find_element(self.SPECIFIC_DATES_OPTION).click()
            # set dates
            # startDate_imput_string = startDate.strftime(self.date_input_format)
            # common.type_and_validate(
            #     self.driver, self.START_DATE_FIELD, startDate_imput_string)

            # endDate_imput_string = endDate.strftime(self.date_input_format)
            # common.type_and_validate(
            #     self.driver, self.END_DATE_FIELD, endDate_imput_string)

            self.browser_lib.press_keys(self.END_DATE_FIELD, "ENTER")

            # parse dates from current url guery params
            current_url = urlparse(self.driver.current_url)
            query_params = parse_qs(current_url.query)
            parsed_startDate_query_param = query_params.get('startDate', [''])[
                0]
            parsed_endDate_query_param = query_params.get('endDate', [''])[0]
            # validate selected dates
            assert parsed_startDate_query_param == startDate.strftime(
                self.date_query_format), "Start date doesn't match"
            assert parsed_endDate_query_param == endDate.strftime(
                self.date_query_format), "End date doesn't match"

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)

    # Expand and count all results
    def expand_and_count_all_results(self):
        try:
            search_show_more_button = self.driver.find_element(
                *self.SHOW_MORE_BUTTON)
            while search_show_more_button and search_show_more_button.is_displayed:
                try:
                    search_show_more_button.click()
                    search_show_more_button = self.driver.find_element(
                        *self.SHOW_MORE_BUTTON)
                except:
                    print("Finish")
                    break

            wait = WebDriverWait(self.driver, timeout=5)

            search_result_list = self.driver.find_element(
                *self.SEARCH_RESULTS_LIST)
            wait.until(lambda d: search_result_list.is_enabled())
            search_result_items = search_result_list.find_elements(
                *self.SEARCH_ITEM)

            print(len(search_result_items))

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)
