from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import constants as const

chrome_options = Options()
chrome_service = Service(executable_path=const.PATH)
# chrome_options.add_experimental_option("detach", True)