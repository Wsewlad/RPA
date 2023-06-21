# import RPA modules
from RPA.Browser.Selenium import Selenium
# import system modules
from urllib.parse import urlparse, parse_qs


class SearchPage:

    dateInputFormat = "%m/%d/%Y"
    dateQueryFormat = "%Y%m%d"

    def __init__(self, browserLib: Selenium):
        self.browserLib = browserLib
        title = self.browserLib.get_title()
        assert title == "The New York Times - Search", "This is not Search Page, current page is - " + \
            self.browserLib.get_location()

    # Set date range
    def set_date_range(self, startDate, endDate):
        try:
            # define selectors
            searchDateDropdown = 'css:[data-testid="search-date-dropdown-a"]'
            specificDates = 'css:[value="Specific Dates"]'
            dateRangeStartDate = 'css:[data-testid="DateRange-startDate"]'
            dateRangeEndDate = 'css:[data-testid="DateRange-endDate"]'

            # navigate to date range picker
            self.browserLib.click_element(searchDateDropdown)
            self.browserLib.click_element(specificDates)

            # set dates
            startDateInputString = startDate.strftime(self.dateInputFormat)
            endDateInputString = endDate.strftime(self.dateInputFormat)

            self.browserLib.input_text(
                dateRangeStartDate, startDateInputString
            )
            self.browserLib.input_text(dateRangeEndDate, endDateInputString)
            self.browserLib.press_keys(dateRangeEndDate, "ENTER")

            # parse dates from current url guery params
            currentUrl = urlparse(self.browserLib.get_location())
            queryParams = parse_qs(currentUrl.query)
            parsedStartDate = queryParams.get('startDate', [''])[
                0]
            parsedEndDate = queryParams.get('endDate', [''])[0]

            # validate selected dates
            assert parsedStartDate == startDate.strftime(
                self.dateQueryFormat), "Start date doesn't match"
            assert parsedEndDate == endDate.strftime(
                self.dateQueryFormat), "End date doesn't match"

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)

    # Expand and count all results
    def expand_and_count_all_results(self):
        try:
            # define selectors
            showMoreButton = 'css:[data-testid="search-show-more-button"]'
            searchResults = 'css:[data-testid="search-results"]'
            searchResult = 'css:[data-testid="search-bodega-result"]'

            # Expand all elements
            while self.browserLib.is_element_visible(showMoreButton):
                try:
                    self.browserLib.click_button(showMoreButton)
                except:
                    print("No more Show Button")
                    break

            self.browserLib.wait_until_element_is_enabled(
                searchResults, timeout=10
            )
            # get all elements
            searchResultList = self.browserLib.find_element(searchResults)
            searchResultEtems = self.browserLib.find_elements(
                searchResult, searchResultList)

            print(len(searchResultEtems))

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)
