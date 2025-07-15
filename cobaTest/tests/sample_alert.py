import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from cobaTest.utils.driver_factory import get_driver

def test_popup_alert():
    driver = get_driver(headless=False)
    driver.get("https://automationtesting.co.uk/popups.html")

    try:
        # Click the button to trigger the alert using XPath with text
        alert_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Trigger Alert')]")
        alert_btn.click()
        time.sleep(1)  # Wait for the alert to appear

        # Switch to alert and accept it
        alert = driver.switch_to.alert
        print(f"Alert text: {alert.text}")
        alert.accept()
        print("Alert appeared and was closed successfully.")
    except NoAlertPresentException:
        print("No alert appeared.")
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_popup_alert()