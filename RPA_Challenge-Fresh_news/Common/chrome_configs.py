from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

PATH = "/Users/vladyslavfil/Downloads/chromedriver_mac64/chromedriver"
chrome_options = Options()
chrome_service = Service(executable_path=PATH)
# chrome_options.add_experimental_option("detach", True)