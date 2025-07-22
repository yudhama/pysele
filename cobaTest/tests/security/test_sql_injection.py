import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from cobaTest.utils.driver_factory import get_driver
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='security_test.log')
logger = logging.getLogger(__name__)

def test_sql_injection():
    """Test for SQL injection vulnerabilities in the CURA Healthcare application"""
    driver = get_driver(headless=False)
    driver.get("https://katalon-demo-cura.herokuapp.com/")
    
    # SQL injection payloads to test
    sql_payloads = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "admin' --",
        "' UNION SELECT 1, username, password FROM users --",
        "'; DROP TABLE users; --"
    ]
    
    try:
        # Navigate to login page
        make_appointment_btn = driver.find_element(By.LINK_TEXT, "Make Appointment")
        make_appointment_btn.click()
        
        # Test SQL injection in login form
        for payload in sql_payloads:
            username_field = driver.find_element(By.ID, "txt-username")
            password_field = driver.find_element(By.ID, "txt-password")
            
            # Clear fields
            username_field.clear()
            password_field.clear()
            
            # Input SQL injection payload
            username_field.send_keys(payload)
            password_field.send_keys(payload)
            
            # Submit form
            login_btn = driver.find_element(By.ID, "btn-login")
            login_btn.click()
            
            # Check if login was successful (which would indicate SQL injection vulnerability)
            if "appointment.php" in driver.current_url:
                logger.critical(f"SQL Injection vulnerability detected with payload: {payload}")
                print(f"SQL Injection vulnerability detected with payload: {payload}")
                
                # If we got in, log out and try the next payload
                menu_toggle = driver.find_element(By.ID, "menu-toggle")
                menu_toggle.click()
                time.sleep(1)
                
                logout_link = driver.find_element(By.LINK_TEXT, "Logout")
                logout_link.click()
                time.sleep(1)
                
                # Navigate back to login page
                make_appointment_btn = driver.find_element(By.LINK_TEXT, "Make Appointment")
                make_appointment_btn.click()
            else:
                # If login failed, we're still on the login page
                logger.info(f"SQL Injection attempt failed with payload: {payload}")
    
    except Exception as e:
        logger.error(f"Test failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_sql_injection()