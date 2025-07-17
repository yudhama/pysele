import os
import time
from selenium.webdriver.common.by import By
from cobaTest.utils.driver_factory import get_driver

def test_upload_sample_txt():
    file_path = "cobaTest/files/sample.txt"
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    driver = get_driver(headless=False)
    driver.get("https://filebin.net/")

    try:
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        # time.sleep(10)  # Wait for the file input to be ready
        file_input.send_keys(os.path.abspath(file_path))
        print(f"Uploaded file: {file_path}")
        time.sleep(3)  # Wait for upload to complete

        # Validation: Check that sample.txt appears in the uploaded files list
        uploaded_file = driver.find_element(By.XPATH, f'//a[contains(text(), "sample.txt")]')
        if uploaded_file:
            print("Validation passed: sample.txt is listed after upload.")
        else:
            print("Validation failed: sample.txt not found after upload.")
    except Exception as e:
        print(f"Failed to upload or validate: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_upload_sample_txt()