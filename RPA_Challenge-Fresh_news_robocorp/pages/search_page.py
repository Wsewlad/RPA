# import RPA modules
from RPA.Browser.Selenium import Selenium
# import system modules
from urllib.parse import urlparse, parse_qs, urlunparse
import re
# import custom modules
import constants as Const


class SearchPage:

    def __init__(self, browserLib: Selenium):
        self.browserLib = browserLib
        title = self.browserLib.get_title()
        assert title == "The New York Times - Search", "This is not Search Page, current page is - " + \
            self.browserLib.get_location()
        self.browserLib.delete_all_cookies()

    def set_date_range(self, startDate, endDate):
        """Set date range."""
        try:
            # Define selectors
            searchDateDropdown = 'css:[data-testid="search-date-dropdown-a"]'
            specificDates = 'css:[value="Specific Dates"]'
            dateRangeStartDate = 'css:[data-testid="DateRange-startDate"]'
            dateRangeEndDate = 'css:[data-testid="DateRange-endDate"]'
            dateRange = 'css:div.query-facet-date button[facet-name="date"]'

            # Navigate to date range picker
            self.browserLib.click_element(searchDateDropdown)
            self.browserLib.click_element(specificDates)

            # Set dates
            startDateInputString = startDate.strftime(Const.DATE_INPUT_FORMAT)
            endDateInputString = endDate.strftime(Const.DATE_INPUT_FORMAT)

            self.browserLib.input_text(
                dateRangeStartDate, startDateInputString
            )
            self.browserLib.input_text(dateRangeEndDate, endDateInputString)
            self.browserLib.press_keys(dateRangeEndDate, "ENTER")

            # Parse dates from current url guery params
            currentUrl = urlparse(self.browserLib.get_location())
            queryParams = parse_qs(currentUrl.query)
            parsedStartDateQuery = queryParams.get('startDate', [''])[0]
            parsedEndDateQuery = queryParams.get('endDate', [''])[0]

            # Add additional dates validation with page reload
            dateRangeValue = self.browserLib.get_element_attribute(
                dateRange, 'value'
            )
            print(dateRangeValue)
            parsedStartDate = re.search(
                "^\d{2}/\d{2}/\d{4}", dateRangeValue).group()
            parsedEndDate = re.search(
                "\d{2}/\d{2}/\d{4}$", dateRangeValue).group()
            matched = startDateInputString == parsedStartDate and endDateInputString == parsedEndDate
            print(matched)
            if matched != dateRangeValue:
                self.browserLib.reload_page()
                # self.browserLib.wait_until_element_contains(
                #     dateRange, startDateInputString)
                # self.browserLib.wait_until_element_contains(
                #     dateRange, endDateInputString)

            dateRangeValue = self.browserLib.get_element_attribute(
                dateRange, 'value'
            )
            print(dateRangeValue)
            parsedStartDate = re.search(
                "^\d{2}/\d{2}/\d{4}", dateRangeValue).group()
            parsedEndDate = re.search(
                "\d{2}/\d{2}/\d{4}$", dateRangeValue).group()

            matched = startDateInputString == parsedStartDate and endDateInputString == parsedEndDate
            print(matched)

            # Validate selected dates
            assert parsedStartDateQuery == startDate.strftime(
                Const.DATE_QUERY_FORMAT), "Start date doesn't match"
            assert parsedEndDateQuery == endDate.strftime(
                Const.DATE_QUERY_FORMAT), "End date doesn't match"

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)

    def expand_and_count_all_results(self):
        """Expand and count all results."""
        try:
            # Define selectors
            showMoreButtonSelector = 'css:[data-testid="search-show-more-button"]'
            searchResultsSelector = 'css:[data-testid="search-results"]'
            searchResultSelector = 'css:[data-testid="search-bodega-result"]'
            searchResultLinkSelector = 'css:[data-testid="search-bodega-result"] a'
            # Expand all elements
            self.__expand_all_elements(
                showMoreButtonSelector, searchResultsSelector
            )
            # Get all elements
            searchResultList = self.browserLib.find_element(
                searchResultsSelector)
            searchResultItems = self.browserLib.find_elements(
                searchResultSelector, searchResultList
            )
            print("count: " + str(len(searchResultItems)))
            # Get unique elements
            uniqueElements = self.__get_unique_elements(
                searchResultItems, searchResultLinkSelector)
            print("unique count: " + str(len(uniqueElements)))

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)

    # Helper Methods

    def __expand_all_elements(self, showMoreButtonSelector, searchResultsSelector):
        """Find and click `Show Button` until it displayed to expand all the elements."""
        self.browserLib.mouse_over(showMoreButtonSelector)
        # Expand all elements
        while self.browserLib.is_element_visible(showMoreButtonSelector):
            try:
                self.browserLib.click_element_when_clickable(
                    showMoreButtonSelector, timeout=10)
                self.browserLib.mouse_over(showMoreButtonSelector)
                # self.browserLib.click_button(showMoreButton)
            except:
                print("No more Show Button")
                break

        self.browserLib.wait_until_element_is_enabled(
            searchResultsSelector, timeout=10
        )

    def __get_unique_elements(self, searchResultItems, searchResultLinkSelector):
        """Extract url subelements, remove query params and filter element by it to get only unique element."""
        # Make Tuple with urls
        tupleItems = [
            (
                element,
                self.__get_clean_url(self.browserLib.find_element(
                    searchResultLinkSelector, element))
            )
            for element in searchResultItems
        ]
        # Filter by unique url
        firstItem = tupleItems.pop(0)
        uniqueTupleItems = [firstItem]
        seenUrls = {firstItem[1]}
        for item in tupleItems:
            if item[1] not in seenUrls:
                uniqueTupleItems.append(item)
                seenUrls.add(item[1])
        return uniqueTupleItems

    def __get_clean_url(self, element) -> str:
        """Parse url from `element` and remove query params."""
        url = urlunparse(list(urlparse(self.browserLib.get_element_attribute(
            element, "href"))[:3]) + ['', '', ''])
        return url
