from selenium.webdriver.common.by import By

class SearchPage:
    SEARCH_DATE_DROPDOWN = (By.CSS_SELECTOR, '[data-testid="search-date-dropdown-a"]')
    SPECIFIC_DATES_OPTION = (By.CSS_SELECTOR, '[value="Specific Dates"]')
    START_DATE_FIELD = (By.CSS_SELECTOR, '[data-testid="DateRange-startDate"]')
    END_DATE_FIELD = (By.CSS_SELECTOR, '[data-testid="DateRange-endDate"]')
    SHOW_MORE_BUTTON = (By.CSS_SELECTOR, '[data-testid="search-show-more-button"]')
    SEARCH_RESULTS_LIST = (By.CSS_SELECTOR, '[data-testid="search-results"]')
    SEARCH_ITEM = (By.CSS_SELECTOR, '[data-testid="search-bodega-result"]')
    
    def __init__(self, driver):
        self.driver = driver
        title = self.driver.title
        assert title == "The New York Times - Search", "This is not Search Page, current page is - " + self.driver.current_url

    # Set date range
    def set_date_range(self, fromDate, toDate):
        try:
            self.driver.find_element(*self.SEARCH_DATE_DROPDOWN).click()
            self.driver.find_element(*self.SPECIFIC_DATES_OPTION).click()

            start_date_field = self.driver.find_element(*self.START_DATE_FIELD)
            start_date_field.send_keys(fromDate)

            end_date_filed = self.driver.find_element(*self.END_DATE_FIELD)
            end_date_filed.send_keys(toDate)

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)

    # Expand and count all results
    def expand_and_count_all_results(self):
        try:
            search_show_more_button = self.driver.find_element(*self.SHOW_MORE_BUTTON)
            while search_show_more_button and search_show_more_button.is_displayed:
                try:
                    search_show_more_button.click()
                    search_show_more_button = self.driver.find_element(*self.SHOW_MORE_BUTTON)
                except:
                    print("Finish")
                    break

            search_result_list = self.driver.find_element(*self.SEARCH_RESULTS_LIST)
            search_result_items = search_result_list.find_elements(*self.SEARCH_ITEM)

            print(len(search_result_items))

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)