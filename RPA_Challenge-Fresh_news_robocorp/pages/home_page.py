
# import RPA modules
from RPA.Browser.Selenium import Selenium

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# import custom modules
import constants as const


class HomePage:
    SEARCH_BUTTON = (By.CSS_SELECTOR, '[data-test-id="search-button"]')
    SEARCH_FIELD = (By.CSS_SELECTOR, '[data-testid="search-input"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-test-id="search-submit"]')

    SEARCH_TEXTFIELD = (By.ID, 'searchTextField')

    def __init__(self, browser_lib: Selenium):
        self.browser_lib = browser_lib

    def lend_first_page(self):
        self.browser_lib.open_available_browser(const.BASE_URL)
        title = self.browser_lib.get_title()
        assert title == "The New York Times - Breaking News, US News, World News and Videos", "This is not Home Page, current page is - " + \
            self.browser_lib.get_location()

    # Search query
    def enter_search_query(self, query):
        try:
            # Type search query
            self.browser_lib.click_element(
                'css:[data-test-id="search-button"]')
            self.browser_lib.input_text_when_element_is_visible(
                'css:[data-testid="search-input"]', query)
            self.browser_lib.click_element(
                'css:[data-test-id="search-submit"]')

            # Validate applied search query on the search page
            searchTextField = 'searchTextField'
            self.browser_lib.wait_until_page_contains_element(searchTextField)

            search_text_field_value = self.browser_lib.get_element_attribute(
                searchTextField, 'value')
            searchTextFieldMatched = self.browser_lib.is_element_attribute_equal_to(
                searchTextField, 'value', query)
            assert searchTextFieldMatched, f"Search text field value [{search_text_field_value}] doesn't match the query [{query}]"

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)
