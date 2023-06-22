# import RPA modules
from RPA.Browser.Selenium import Selenium
# import custom modules
import constants as const


class HomePage:

    def __init__(self, browserLib: Selenium):
        self.browserLib = browserLib

    def lend_first_page(self):
        """Navigate to home page."""

        self.browserLib.open_available_browser(const.BASE_URL)
        title = self.browserLib.get_title()
        assert title == "The New York Times - Breaking News, US News, World News and Videos", "This is not Home Page, current page is - " + \
            self.browserLib.get_location()

    def enter_search_query(self, query):
        """Enter search query."""
        try:
            # Define selectors
            searchButton = 'css:[data-test-id="search-button"]'
            searchInput = 'css:[data-testid="search-input"]'
            searchSubmit = 'css:[data-test-id="search-submit"]'
            searchTextField = 'searchTextField'

            # Type search query
            self.browserLib.click_element(searchButton)
            self.browserLib.input_text_when_element_is_visible(
                searchInput, query
            )
            self.browserLib.click_element(searchSubmit)

            # Validate applied search query on the search page
            self.browserLib.wait_until_page_contains_element(searchTextField)
            searchTextFieldValue = self.browserLib.get_element_attribute(
                searchTextField, 'value'
            )
            searchTextFieldMatched = self.browserLib.is_element_attribute_equal_to(
                searchTextField, 'value', query
            )

            assert searchTextFieldMatched, f"Search text field value [{searchTextFieldValue}] doesn't match the query [{query}]"

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)
