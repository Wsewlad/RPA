import os

from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from RPA.PDF import PDF

browser_lib = Selenium()
browser_lib.set_selenium_implicit_wait(15)


def open_the_intranet_website():
    browser_lib.open_available_browser("https://robotsparebinindustries.com/")
    browser_lib.auto_close = False


def log_in():

    browser_lib.input_text("username", "maria")
    browser_lib.input_text("password", "thoushallnotpass")
    browser_lib.submit_form()
    browser_lib.wait_until_page_contains_element("sales-form")


def download_the_excel_file():
    http = HTTP()
    http.download(
        url="https://robotsparebinindustries.com/SalesData.xlsx",
        overwrite=True)


def fill_and_submit_the_form_for_one_person(sales_rep):
    browser_lib.input_text("firstname", sales_rep["First Name"])
    browser_lib.input_text("lastname", sales_rep["Last Name"])
    browser_lib.input_text("salesresult", str(sales_rep["Sales"]))
    browser_lib.select_from_list_by_value(
        "salestarget",
        str(sales_rep["Sales Target"]))
    browser_lib.click_button("Submit")


def fill_the_form_using_the_data_from_the_excel_file():
    excel = Files()
    excel.open_workbook("SalesData.xlsx")
    sales_reps = excel.read_worksheet_as_table(header=True)
    excel.close_workbook()
    for sales_rep in sales_reps:
        fill_and_submit_the_form_for_one_person(sales_rep)


def collect_the_results():
    browser_lib.screenshot(
        "css:div.sales-summary",
        f"{os.getcwd()}/output/sales_summary.png")


def export_the_table_as_a_pdf():
    sales_results_html = browser_lib.get_element_attribute(
        "css:#sales-results",
        "outerHTML"
    )
    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/sales_results.pdf")


def log_out():
    browser_lib.click_button("Log out")


def main():
    try:
        open_the_intranet_website()
        log_in()
        download_the_excel_file()
        fill_the_form_using_the_data_from_the_excel_file()
        collect_the_results()
        export_the_table_as_a_pdf()
    finally:
        print("Finish")
        # log_out()
        # browser_lib.close_browser()


if __name__ == "__main__":
    main()
