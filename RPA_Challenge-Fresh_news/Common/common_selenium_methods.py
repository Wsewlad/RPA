from selenium.webdriver.common.by import By

def type_and_validate(driver, selector, text):
    search_field = driver.find_element(*selector)
    search_field.clear()
    search_field_typed_value = search_field.get_attribute("value")

    assert search_field_typed_value == text, f"Typed text doesn't match for: {selector}"