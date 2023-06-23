# import RPA modules
from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Excel.Files import Files
# import system modules
import os
from urllib.parse import urlparse
# import pages
from pages.home_page import HomePage
from pages.search_page import SearchPage
# import custom modules
from common.Dates import get_date_range
import common.Helpers as helpers
from common.Decorators import step_logger_decorator


def make_row(date, title, description, pictureUrl, searchPhrase):
    """Constract a row for excel table."""
    row = {
        'Date': date,
        'Title': title,
        'Search Phrases Count': helpers.count_query_occurrences(searchPhrase, title, description),
        'Description': description or 'No description found',
        'Contains Money': helpers.contains_money(title, description),
        'Picture Filename': helpers.get_file_name_from_url(pictureUrl) or "No picture found"
    }
    return row


@step_logger_decorator("Create And Fill Excel File")
def create_and_fill_excel_file(searchPage, searchPhrase, articles):
    """Parse articles data and create excel file with it. Download article pictures."""
    try:
        excelLib = Files()
        excelLib.create_workbook(
            path=os.path.join('output', 'articles.xlsx'), fmt="xlsx", sheet_name="NYT")
        data = []
        for article in articles:
            try:
                # Parse article data
                title, date, description, pictureUrl = searchPage.parse_article_data(
                    article[0])
                # Download picture
                if pictureUrl:
                    helpers.download_picture(
                        pictureUrl, os.path.join('output', 'images'))
                else:
                    print(f'No picture found for: {title}')
                if not description:
                    print(f'No description found for: {title}')
                # Create and append article data row
                row = make_row(
                    date, title, description, pictureUrl, searchPhrase
                )
                data.append(row)
            except Exception as e:
                print(f"Failed to parse article data: {article[1]}", e)
    except Exception as e:
        print("Failed collecting articles data", e)
    finally:
        # Save data
        excelLib.append_rows_to_worksheet(data, header=True)
        excelLib.save_workbook()


def main():
    try:
        # Retrieve work items
        library = WorkItems()
        library.get_input_work_item()
        variables = library.get_work_item_variables()

        searchPhrase: str = variables["search_phrase"]
        categories: list = variables.get("categories", [])
        sections: list = variables.get("sections", [])
        numberOfMonth: int = variables.get("number_of_month", 0)
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
        # Set filters
        if len(categories) > 0:
            searchPage.set_filters(categories, 'type')
        else:
            print("No category filters provided")
        if len(sections) > 0:
            searchPage.set_filters(sections, 'section')
        else:
            print("No section filters provided")
        searchPage.set_date_range(startDate, endDate)
        searchPage.sort_by_newest()
        # Get all unique articles
        articles = searchPage.expand_and_get_all_articles()
        if len(articles) == 0:
            print("No articles")
            return
        # Create  Excel file and download pictures
        create_and_fill_excel_file(searchPage, searchPhrase, articles)

    except Exception as e:
        print("Error:", e)
    finally:
        print("End")
        # browser_lib.close_all_browsers()


if __name__ == "__main__":
    main()
