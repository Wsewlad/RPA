# import RPA modules
from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
# import system modules
import re
import os
from urllib.parse import urlparse
# import pages
from pages.home_page import HomePage
from pages.search_page import SearchPage
# import custom modules
from common.Dates import get_date_range


def contains_money(title, description):
    # Define the regex pattern to match money amounts
    pattern = r'\$[\d,.]+|\d+\s?(dollars|USD)'
    # Combine the title and description into a single string
    text = title + ' ' + description
    # Search for matches using the regex pattern
    matches = re.findall(pattern, text)
    # Check if any matches were found
    if matches:
        return True
    else:
        return False


def get_file_name_from_url(url):
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    return file_name


def download_the_picture(url: str, path: str):
    http = HTTP()
    http.download(
        url=url,
        target_file=os.path.join(path, get_file_name_from_url(url)),
        overwrite=True)


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
        articles = searchPage.expand_and_get_all_articles()

        if len(articles) == 0:
            print("No articles")
            return

        try:
            excelLib = Files()
            excelLib.create_workbook(
                path=os.path.join('output', 'articles.xlsx'), fmt="xlsx", sheet_name="NYT")
            data = []
            for article in articles:
                try:
                    title, date, description, pictureUrl = searchPage.parse_article_data(
                        article[0])
                    download_the_picture(
                        pictureUrl, os.path.join('output', 'images'))
                    row = {
                        'Date': date,
                        'Title': title,
                        'Search Phrases Count': title.count(searchPhrase) + description.count(searchPhrase),
                        'Description': description,
                        'Contains Money': contains_money(title, description),
                        'Picture Filename': get_file_name_from_url(pictureUrl)
                    }
                    data.append(row)
                except Exception as e:
                    print(f"failed to parse article data: {article[1]}", e)
        except Exception as e:
            print("Failed collecting articles data", e)
        finally:
            excelLib.append_rows_to_worksheet(data, header=True)
            excelLib.save_workbook()

    except Exception as e:
        print("Error:", e)
    finally:
        print("End")
        # browser_lib.close_all_browsers()


if __name__ == "__main__":
    main()
