from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import common.common_selenium_methods as common
import constants as const

class HomePage:
    SEARCH_BUTTON = (By.CSS_SELECTOR, '[data-test-id="search-button"]')
    SEARCH_FIELD = (By.CSS_SELECTOR, '[data-testid="search-input"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-test-id="search-submit"]')

    SEARCH_TEXTFIELD = (By.ID, 'searchTextField')

    def __init__(self, driver):
        self.driver = driver
        
    def lend_first_page(self):
        self.driver.get(const.BASE_URL)
        title = self.driver.title
        assert title == "The New York Times - Breaking News, US News, World News and Videos", "This is not Home Page, current page is - " + self.driver.current_url

    # Search query
    def enter_search_query(self, query):
        try:
            ## Type search query
            self.driver.find_element(*self.SEARCH_BUTTON).click()
            common.type_and_validate(self.driver, self.SEARCH_FIELD, query)
            self.driver.find_element(*self.SUBMIT_BUTTON).click()

            ## Validate applied search query on the search page
            wait = WebDriverWait(self.driver, timeout=10)
            search_text_field = self.driver.find_element(*self.SEARCH_TEXTFIELD)
            wait.until(lambda d : search_text_field.is_displayed())  
            search_text_field_value = search_text_field.get_attribute("value")
            assert search_text_field_value == query, f"Search text field value [{search_text_field_value}] doesn't match the query [{query}]"

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)
