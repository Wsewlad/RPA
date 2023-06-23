# import RPA modules
from RPA.Browser.Selenium import Selenium
# import system modules
from urllib.parse import urlparse, parse_qs, urlunparse
import re
# import custom modules
import constants as Const
from common.Decorators import exception_decorator, step_logger_decorator


class SearchPage:

    def __init__(self, browser_lib: Selenium):
        self.browser_lib = browser_lib
        title = self.browser_lib.get_title()
        assert title == "The New York Times - Search", "This is not Search Page, current page is - " + \
            self.browser_lib.get_location()
        self.browser_lib.delete_all_cookies()

    @exception_decorator("Set Date Range")
    @step_logger_decorator("Set Date Range")
    def set_date_range(self, start_date, end_date):
        """Set date range."""
        # Define selectors
        search_date_dropdown_selector = 'css:[data-testid="search-date-dropdown-a"]'
        specific_dates_selector = 'css:[value="Specific Dates"]'
        date_range_start_date_selector = 'css:[data-testid="DateRange-startDate"]'
        date_range_end_date_selector = 'css:[data-testid="DateRange-endDate"]'

        # Navigate to date range picker
        self.browser_lib.click_element(search_date_dropdown_selector)
        self.browser_lib.click_element(specific_dates_selector)

        # Get date strings in appropriate format
        start_date_input_string = start_date.strftime(Const.DATE_INPUT_FORMAT)
        end_date_input_string = end_date.strftime(Const.DATE_INPUT_FORMAT)
        start_date_query_string = start_date.strftime(Const.DATE_QUERY_FORMAT)
        end_date_query_string = end_date.strftime(Const.DATE_QUERY_FORMAT)

        # Input dates
        self.browser_lib.input_text(
            date_range_start_date_selector, start_date_input_string
        )
        self.browser_lib.input_text(
            date_range_end_date_selector, end_date_input_string)
        self.browser_lib.press_keys(date_range_end_date_selector, "ENTER")

        # Validate selected dates
        self.__verify_date_entries(
            start_date_input_string, end_date_input_string, start_date_query_string, end_date_query_string)

    @exception_decorator("Set Filters")
    @step_logger_decorator("Set Filters")
    def set_filters(self, items: list[str], filter_type: str):
        """Set filters and verify if selected."""

        if filter_type not in ['type', 'section']:
            raise Exception(f"Undefined filter type: {filter_type}")

        # Define selectors
        form_selector = f'css:[role="form"][data-testid="{filter_type}"]'
        button_selector = 'css:button[data-testid="search-multiselect-button"]'
        dropdown_list_selector = 'css:[data-testid="multi-select-dropdown-list"]'
        checkbox_selector = 'css:input[type="checkbox"]'

        # Open dropdown list
        type_form_element = self.browser_lib.find_element(form_selector)
        button_element = self.browser_lib.find_element(
            button_selector, type_form_element)
        self.browser_lib.click_element(button_element)

        # Wait for dropdown list
        dropdown_list_element = self.browser_lib.find_element(
            dropdown_list_selector, type_form_element)
        self.browser_lib.wait_until_element_is_visible(dropdown_list_element)

        # Find all checkbox elements and map it by value
        checkbox_elements = self.browser_lib.find_elements(
            checkbox_selector, dropdown_list_element)
        checkbox_by_value: dict[str, any] = dict([
            (
                self.__format_item(
                    self.browser_lib.get_element_attribute(
                        checkbox, 'value'
                    ).split('|nyt:', 1)[0]
                ),
                checkbox
            )
            for checkbox in checkbox_elements
        ])

        # If categories contains `Any` - skip selecting
        unique_items = set(items)
        formatted_items = set(
            [
                self.__format_item(category)
                for category in unique_items
            ]
        )
        if "any" in formatted_items:
            return

        # Select items and save not_found_items
        not_found_items = []
        for category in unique_items:
            try:
                formatted_category = self.__format_item(category)
                self.browser_lib.click_element(
                    checkbox_by_value[formatted_category])
            except:
                not_found_items.append(category)
        print("Unknown filters: ", not_found_items)

        # Verify selected items
        self.__verify_selected_items(
            not_found_items, formatted_items, filter_type)

    @exception_decorator("Sort By Newest")
    @step_logger_decorator("Sort By Newest")
    def sort_by_newest(self):
        """Sort articles by newest."""
        # Define selectors
        sortBySelector = 'css:[data-testid="SearchForm-sortBy"]'

        # Select
        valueToSelect = 'newest'
        self.browserLib.select_from_list_by_value(
            sortBySelector, valueToSelect)

        # Verify
        sortByElementValue = self.browserLib.get_selected_list_value(
            sortBySelector)
        assert sortByElementValue == valueToSelect

    @exception_decorator("Expand And Get All Articles")
    @step_logger_decorator("Expand And Get All Articles")
    def expand_and_get_all_articles(self) -> list[tuple[any, str]]:
        """Expand and count all results."""
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
        print("All articles count: " + str(len(searchResultItems)))

        # Get unique elements
        uniqueElements = self.__get_unique_elements(
            searchResultItems, searchResultLinkSelector)
        print("Unique articles count: " + str(len(uniqueElements)))
        return uniqueElements

    @exception_decorator("Parse Article Data")
    def parse_article_data(self, articleElement):
        """Parse article's data"""
        # Define selectors
        dateSelector = 'css:[data-testid="todays-date"]'
        titleSelector = 'css:a > h4'
        descriptionSelector = 'css:a p:nth-child(2)'
        imageSelector = 'css:img'

        # Get data
        dateElement = self.browserLib.find_element(
            dateSelector, articleElement)
        date = self.browserLib.get_text(dateElement)
        titleElement = self.browserLib.find_element(
            titleSelector, articleElement)
        title = self.browserLib.get_text(titleElement)
        try:
            descriptionElement = self.browserLib.find_element(
                descriptionSelector, articleElement)
            description = self.browserLib.get_text(descriptionElement)
        except:
            description = None
        try:
            imageElement = self.browserLib.find_element(
                imageSelector, articleElement)
            imageUrl = self.__get_clean_url(
                self.browserLib.get_element_attribute(imageElement, 'src')
            )
        except:
            imageUrl = None

        return title, date, description, imageUrl

    # Helper Methods

    def __format_item(self, item: str) -> str:
        return item.replace(" ", "").lower()

    def __verify_selected_items(self, notFoundItems, formattedItems, type: str):
        """Verify selected items."""

        # Define selectors
        selectedItemContainerSelector = f'css:div.query-facet-{type}s'
        selectedItemSelector = f'css:button[facet-name="{type}s"]'

        # Find container
        selectedItemsContainerElement = self.browserLib.find_element(
            selectedItemContainerSelector)

        # Find elements
        selectedItemElements = self.browserLib.find_elements(
            selectedItemSelector, selectedItemsContainerElement)

        # Get element values
        selectedItemsLabels = [
            self.__format_item(self.browserLib.get_element_attribute(
                category, 'value').split('|nyt:', 1)[0])
            for category in selectedItemElements
        ]
        notFoundItemsFormatted = [
            self.__format_item(item) for item in notFoundItems]
        expectedSelectedItems = [
            item for item in formattedItems if item not in notFoundItemsFormatted]

        # Verify
        assert len(set(expectedSelectedItems).intersection(selectedItemsLabels)) == len(
            expectedSelectedItems), f"Selected {type} items doesn't match"

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

    def __get_unique_elements(self, searchResultItems, searchResultLinkSelector) -> list[tuple[any, str]]:
        """Extract url subelements, remove query params and filter element by it to get only unique element."""

        # Make Tuple with urls
        tupleItems = [
            (
                element,
                self.__get_clean_url(
                    self.browserLib.get_element_attribute(
                        self.browserLib.find_element(
                            searchResultLinkSelector, element),
                        'href'
                    )
                )
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

    def __get_clean_url(self, url) -> str:
        """Remove query params from url."""

        cleanUrl = urlunparse(list(urlparse(url)[:3]) + ['', '', ''])
        return cleanUrl
