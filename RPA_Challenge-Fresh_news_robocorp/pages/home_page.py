# import RPA modules
from RPA.Browser.Selenium import Selenium
# import custom modules
import constants as const


class HomePage:

    def __init__(self, browser_lib: Selenium):
        self.browser_lib = browser_lib

    # Navigate
    def lend_first_page(self):
        self.browser_lib.open_available_browser(const.BASE_URL)
        title = self.browser_lib.get_title()
        assert title == "The New York Times - Breaking News, US News, World News and Videos", "This is not Home Page, current page is - " + \
            self.browser_lib.get_location()

    # Search query
    def enter_search_query(self, query):
        try:
            # define selectors
            search_button = 'css:[data-test-id="search-button"]'
            search_input = 'css:[data-testid="search-input"]'
            search_submit = 'css:[data-test-id="search-submit"]'
            searchTextField = 'searchTextField'

            # Type search query
            self.browser_lib.click_element(search_button)
            self.browser_lib.input_text_when_element_is_visible(
                search_input, query)
            self.browser_lib.click_element(search_submit)

            # Validate applied search query on the search page
            self.browser_lib.wait_until_page_contains_element(searchTextField)
            search_text_field_value = self.browser_lib.get_element_attribute(
                searchTextField, 'value')
            searchTextFieldMatched = self.browser_lib.is_element_attribute_equal_to(
                searchTextField, 'value', query)

            assert searchTextFieldMatched, f"Search text field value [{search_text_field_value}] doesn't match the query [{query}]"

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)
