# import RPA modules
import sys
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
            raise Exception(f'[{self.__class__.__name__}]',
                            e, sys.exc_info()[-1].tb_lineno)

    def set_filters(self, items: list[str], type: str):
        """Set filters and verify if selected."""
        try:
            if type not in ['type', 'section']:
                raise Exception(f"Undefined filter type: {type}")

            # Define selectors
            formSelector = f'css:[role="form"][data-testid="{type}"]'
            buttonSelector = 'css:button[data-testid="search-multiselect-button"]'
            dropdownListSelector = 'css:[data-testid="multi-select-dropdown-list"]'
            checkboxSelector = 'css:input[type="checkbox"]'

            # Open dropdown list
            typeFormElement = self.browserLib.find_element(formSelector)
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
                    self.__format_item(
                        self.browserLib.get_element_attribute(
                            checkbox, 'value'
                        ).split('|nyt:', 1)[0]
                    ),
                    checkbox
                )
                for checkbox in checkboxElements
            ])

            # If categories contains `Any` - skip selecting
            uniqueItems = set(items)
            formattedItems = set(
                [
                    self.__format_item(category)
                    for category in uniqueItems
                ]
            )
            if "any" in formattedItems:
                return

            # Select items and save notFoundItems
            notFoundItems = []
            for category in uniqueItems:
                try:
                    formattedCategory = self.__format_item(category)
                    self.browserLib.click_element(
                        checkboxByValue[formattedCategory])
                except:
                    notFoundItems.append(category)
            print("Not found: ", notFoundItems)

            # Verify selected items
            self.__verify_selected_items(
                notFoundItems, formattedItems, type)
        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]',
                            e, sys.exc_info()[-1].tb_lineno)

    def sort_by_newest(self):
        """Sort articles by newest."""
        try:
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
        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]',
                            e, sys.exc_info()[-1].tb_lineno)

    def expand_and_get_all_articles(self) -> list[tuple[any, str]]:
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
            return uniqueElements

        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]',
                            e, sys.exc_info()[-1].tb_lineno)

    def parse_article_data(self, articleElement):
        """Parse article's data"""
        try:
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
            descriptionElement = self.browserLib.find_element(
                descriptionSelector, articleElement)
            description = self.browserLib.get_text(descriptionElement)
            imageElement = self.browserLib.find_element(
                imageSelector, articleElement)
            imageUrl = self.__get_clean_url(
                self.browserLib.get_element_attribute(imageElement, 'src')
            )

            return title, date, description, imageUrl
        except Exception as e:
            raise Exception(f'[{self.__class__.__name__}]',
                            e, sys.exc_info()[-1].tb_lineno)

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
        """Parse url from `element` and remove query params."""

        cleanUrl = urlunparse(list(urlparse(url)[:3]) + ['', '', ''])
        return cleanUrl
