# import RPA modules
from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems
# import system modules
# import pages
from pages.home_page import HomePage
from pages.search_page import SearchPage
# import custom modules
from common.Dates import get_date_range


def main():
    try:
        # Retrieve work items
        library = WorkItems()
        library.get_input_work_item()
        variables = library.get_work_item_variables()

        searchPhrase: str = variables["search_phrase"]
        categories: list[str] = variables["categories"]
        sections: list[str] = variables["sections"]
        numberOfMonth: int = variables["number_of_month"] | 0
        startDate, endDate = get_date_range(numberOfMonth)

        # Init browser lib
        browserLib: Selenium = Selenium()
        browserLib.auto_close = False

        # Home page logic
        homePage = HomePage(browserLib)
        homePage.lend_first_page()
        homePage.enter_search_query(searchPhrase)

        # Search page logic
        searchPage = SearchPage(browserLib)

        if len(categories) > 0:
            searchPage.set_filters(categories, 'type')
        else:
            print("No categories")

        if len(sections) > 0:
            searchPage.set_filters(sections, 'section')
        else:
            print("No sections")
        searchPage.set_date_range(startDate, endDate)
        searchPage.sort_by_newest()
        searchPage.expand_and_count_all_results()

    except Exception as e:
        print("Error:", e)
    finally:
        print("End")
        # browser_lib.close_all_browsers()


if __name__ == "__main__":
    main()
