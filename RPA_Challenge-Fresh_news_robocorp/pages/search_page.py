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
            searchDateDropdownSelector = 'css:[data-testid="search-date-dropdown-a"]'
            specificDatesSelector = 'css:[value="Specific Dates"]'
            dateRangeStartDateSelector = 'css:[data-testid="DateRange-startDate"]'
            dateRangeEndDateSelector = 'css:[data-testid="DateRange-endDate"]'

            # Navigate to date range picker
            self.browserLib.click_element(searchDateDropdownSelector)
            self.browserLib.click_element(specificDatesSelector)

            # Get date strings in appropriate format
            startDateInputString = startDate.strftime(Const.DATE_INPUT_FORMAT)
            endDateInputString = endDate.strftime(Const.DATE_INPUT_FORMAT)
            startDateQueryString = startDate.strftime(Const.DATE_QUERY_FORMAT)
            endDateQueryString = endDate.strftime(Const.DATE_QUERY_FORMAT)
            # Input dates
            self.browserLib.input_text(
                dateRangeStartDateSelector, startDateInputString
            )
            self.browserLib.input_text(
                dateRangeEndDateSelector, endDateInputString)
            self.browserLib.press_keys(dateRangeEndDateSelector, "ENTER")
            # Validate selected dates
            self.__verify_date_entries(
                startDateInputString, endDateInputString, startDateQueryString, endDateQueryString)
        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]', e)

    def set_categories(self, categories: list[str]):
        """Set categories and verify if selected."""
        # Define selectors
        typeFormSelector = 'css:[role="form"][data-testid="type"]'
        buttonSelector = 'css:button[data-testid="search-multiselect-button"]'
        dropdownListSelector = 'css:[data-testid="multi-select-dropdown-list"]'
        checkboxSelector = 'css:input[type="checkbox"]'
        # Open dropdown list
        typeFormElement = self.browserLib.find_element(typeFormSelector)
        buttonElement = self.browserLib.find_element(
            buttonSelector, typeFormElement)
        self.browserLib.click_element(buttonElement)
        # Wait for dropdown list
        dropdownListElement = self.browserLib.find_element(
            dropdownListSelector, typeFormElement)
        self.browserLib.wait_until_element_is_visible(dropdownListElement)
        # Find all checkbox elements and map it by value
        checkboxElements = self.browserLib.find_elements(
            checkboxSelector, dropdownListElement)
        checkboxByValue: dict[str, any] = dict([
            (
                self.browserLib.get_element_attribute(checkbox, 'value'),
                checkbox
            )
            for checkbox in checkboxElements
        ])
        # If categories contains `Any`` - skip selecting
        uniqueCategories = set(categories)
        formattedCategories = set([category.replace(
            " ", "").lower() for category in uniqueCategories])
        if "any" in formattedCategories:
            return
        # Select categories and save notFoundCategories
        notFoundCategories = []
        for category in uniqueCategories:
            try:
                formattedCategory = category.replace(" ", "").lower()
                self.browserLib.click_element(
                    checkboxByValue[formattedCategory])
            except:
                notFoundCategories.append(category)
        print("Not found: ", notFoundCategories)
        # Verify selected categories
        self.__verify_selected_categories(
            notFoundCategories, formattedCategories)

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

    def __verify_selected_categories(self, notFoundCategories, formattedCategories):
        """Verify selected categories."""
        # Define selectors
        selectedCategoriesContainerSelector = 'css:div.query-facet-types'
        selectedCategorySelector = 'css:button[facet-name="types"]'
        # Find container
        selectedCategoriesContainerElement = self.browserLib.find_element(
            selectedCategoriesContainerSelector)
        # Find elements
        selectedCategoryElements = self.browserLib.find_elements(
            selectedCategorySelector, selectedCategoriesContainerElement)
        # Get element values
        selectedCategoriesLabels = [
            self.browserLib.get_element_attribute(category, 'value')
            for category in selectedCategoryElements
        ]
        notFoundCategoriesFormatted = [category.replace(
            " ", "").lower() for category in notFoundCategories]
        expectedSelectedCategories = [
            category for category in formattedCategories if category not in notFoundCategoriesFormatted]
        # Verify
        assert len(set(expectedSelectedCategories).intersection(selectedCategoriesLabels)) == len(
            expectedSelectedCategories), "Selected categories doesn't match"

    def __verify_date_entries(self, startDateInputString: str, endDateInputString: str, startDateQueryString: str, endDateQueryString: str):
        """Parse and validate dates from the current URL query parameters and perform additional validation with page reload."""
        # Parse dates from current url guery params
        currentUrl = urlparse(self.browserLib.get_location())
        queryParams = parse_qs(currentUrl.query)
        parsedStartDateQuery = queryParams.get('startDate', [''])[0]
        parsedEndDateQuery = queryParams.get('endDate', [''])[0]
        # Validate date range from query params
        assert parsedStartDateQuery == startDateQueryString, "Start date doesn't match"
        assert parsedEndDateQuery == endDateQueryString, "End date doesn't match"
        # Validate date range from UI
        matched = self.__parse_and_verify_date_range_from_ui(
            startDateInputString, endDateInputString)
        if not matched:
            self.browserLib.reload_page()
        matched = self.__parse_and_verify_date_range_from_ui(
            startDateInputString, endDateInputString)
        assert matched, "Date range from UI doesn't match"

    def __parse_and_verify_date_range_from_ui(self, startDateInputString: str, endDateInputString: str) -> bool:
        """Find, parse and validate date range from UI"""
        # Define selectors
        dateRangeSelector = 'css:div.query-facet-date button[facet-name="date"]'
        # Get date range from UI element
        dateRangeValue = self.browserLib.get_element_attribute(
            dateRangeSelector, 'value'
        )
        # Parse start and end dates
        parsedStartDate = re.search(
            "^\d{2}/\d{2}/\d{4}", dateRangeValue).group()
        parsedEndDate = re.search(
            "\d{2}/\d{2}/\d{4}$", dateRangeValue).group()
        # Validate
        matched = startDateInputString == parsedStartDate and endDateInputString == parsedEndDate
        return matched

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
