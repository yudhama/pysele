import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cobaTest.utils.driver_factory import get_driver
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='security_test.log')
logger = logging.getLogger(__name__)

def test_authentication_security():
    """Test for authentication security vulnerabilities"""
    driver = get_driver(headless=False)
    driver.get("https://katalon-demo-cura.herokuapp.com/")
    
    try:
        # Navigate to login page
        make_appointment_btn = driver.find_element(By.LINK_TEXT, "Make Appointment")
        make_appointment_btn.click()
        
        # Test 1: Brute force protection
        logger.info("Testing brute force protection...")
        for i in range(5):  # Try 5 incorrect login attempts
            username_field = driver.find_element(By.ID, "txt-username")
            password_field = driver.find_element(By.ID, "txt-password")
            
            username_field.clear()
            password_field.clear()
            
            username_field.send_keys("John Doe")
            password_field.send_keys(f"wrong_password_{i}")
            
            login_btn = driver.find_element(By.ID, "btn-login")
            login_btn.click()
            
            # Check if there's any rate limiting or account lockout
            error_message = driver.find_element(By.CSS_SELECTOR, ".text-danger").text
            logger.info(f"Attempt {i+1} error message: {error_message}")
            
            # If there's a lockout message or CAPTCHA, report it
            if "locked" in error_message.lower() or "too many attempts" in error_message.lower():
                logger.info("Brute force protection detected: Account lockout")
                break
        
        # Test 2: Direct page access without authentication
        logger.info("Testing direct page access...")
        driver.get("https://katalon-demo-cura.herokuapp.com/#appointment")
        
        # Check if we're redirected to login
        current_url = driver.current_url
        if "profile.php#login" in current_url:
            logger.info("Authentication check passed: Redirected to login when accessing protected page")
        else:
            logger.critical("Authentication vulnerability: Can access appointment page without login")
            print("Authentication vulnerability: Can access appointment page without login")
        
        # Test 3: Session handling after logout
        logger.info("Testing session handling after logout...")
        
        # First login properly
        driver.get("https://katalon-demo-cura.herokuapp.com/profile.php#login")
        username_field = driver.find_element(By.ID, "txt-username")
        password_field = driver.find_element(By.ID, "txt-password")
        
        username_field.clear()
        password_field.clear()
        
        username_field.send_keys("John Doe")
        password_field.send_keys("ThisIsNotAPassword")
        
        login_btn = driver.find_element(By.ID, "btn-login")
        login_btn.click()
        
        # Verify we're logged in
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "combo_facility"))
        )
        
        # Now logout
        menu_toggle = driver.find_element(By.ID, "menu-toggle")
        menu_toggle.click()
        time.sleep(1)
        
        logout_link = driver.find_element(By.LINK_TEXT, "Logout")
        logout_link.click()
        time.sleep(1)
        
        # Try to access appointment page again by using browser back button
        driver.back()
        driver.back()
        
        # Check if we're redirected to login again
        current_url = driver.current_url
        if "profile.php#login" in current_url:
            logger.info("Session handling check passed: Session invalidated after logout")
        else:
            logger.critical("Session handling vulnerability: Can access protected page after logout")
            print("Session handling vulnerability: Can access protected page after logout")
    
    except Exception as e:
        logger.error(f"Test failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_authentication_security()