from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

try: 
    driver.get("https://vinothqaacademy.com/alert-and-popup/")
    time.sleep(3)  # Wait for the page to load
    driver.find_element(By.NAME, "promptalertbox1234").click()
    alert = driver.switch_to.alert
    alert.send_keys("")
    print(f"Alert text: {alert.text}")

    alert.send_keys("yes")
    print(f"Alert text: {alert.text}")
    # time.sleep(2)  # Wait for the alert to be processed
    alert.accept()
    time.sleep(2)  # Wait for the alert to be processed
    print("Alert accepted with input.")
    result = driver.find_element(By.ID, "demoone").text
    print(f"Result after alert: {result}")  
    assert "Thanks for Liking Automation" in result, "Alert input was processed correctly."

    driver.find_element(By.NAME, "promptalertbox1234").click()
    alert = driver.switch_to.alert
    print(f"Alert text: {alert.text}")
    time.sleep(2)  # Wait for the alert to be processed
    alert.send_keys("no")
    print(f"Alert text: {alert.text}")
    # time.sleep(3)  # Wait for the alert to be processed
    alert.accept()
    time.sleep(2)  # Wait for the alert to be processed
    result = driver.find_element(By.ID, "demoone").text
    print(f"Result after alert: {result}")  
    assert "Sad to hear it !" in result, "Alert input was not processed correctly."
    # driver.find_element(By.ID, "demoone").get_attribute("")
    

finally:
    driver.quit()
    print("Browser closed.")    