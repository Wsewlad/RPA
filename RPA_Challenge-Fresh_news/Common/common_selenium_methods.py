from selenium.webdriver.common.by import By
from screeninfo import get_monitors

def type_and_validate(driver, selector, text):
    search_field = driver.find_element(*selector)
    search_field.clear()
    search_field.send_keys(text)
    search_field_typed_value = search_field.get_attribute("value")

    assert search_field_typed_value == text, f"Typed text doesn't match for: {selector}"


def get_second_monitor_position():
    monitors = get_monitors()
    secondary_monitors = [monitor for monitor in monitors if not monitor.is_primary]
    x = 0
    y = 0
    if secondary_monitors:
        x = secondary_monitors[0].x
        y = secondary_monitors[0].y
    return (x, y)