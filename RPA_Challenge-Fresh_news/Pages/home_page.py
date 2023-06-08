from selenium.webdriver.common.by import By

class HomePage:
    SEARCH_BUTTON = (By.CSS_SELECTOR, '[data-test-id="search-button"]')
    SEARCH_FIELD = (By.CSS_SELECTOR, '[data-testid="search-input"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-test-id="search-submit"]')

    def __init__(self, driver):
        self.driver = driver
        title = self.driver.title
        assert title == "The New York Times - Breaking News, US News, World News and Videos", "This is not Home Page, current page is - " + self.driver.current_url

    ## Search query
    def enter_search_query(self, query):
        try:
            self.driver.find_element(*self.SEARCH_BUTTON).click()
            search_field = self.driver.find_element(*self.SEARCH_FIELD)
            search_field.send_keys(query)

            search_field_typed_value = search_field.get_attribute("value")

            assert search_field_typed_value == query, "Typed search query doesn't match"

            self.driver.find_element(*self.SUBMIT_BUTTON).click()
        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)
