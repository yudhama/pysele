"""
Enhanced CURA Healthcare Service - Appointment Automation Script
This version includes automatic ChromeDriver management and better error handling.
"""

import time
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cura_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CURAAppointmentBot:
    """Enhanced automation bot for CURA Healthcare appointment booking"""
    
    def __init__(self, headless=False, wait_timeout=15):
        """Initialize the automation bot"""
        self.base_url = "https://katalon-demo-cura.herokuapp.com/"
        self.wait_timeout = wait_timeout
        self.driver = None
        self.headless = headless
        self.credentials = {
            "username": "John Doe",
            "password": "ThisIsNotAPassword"
        }
        
    def setup_driver(self):
        """Setup Chrome driver with automatic driver management"""
        try:
            logger.info("Setting up Chrome driver...")

            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")

            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            chrome_options = Options()

            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            }

            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-save-password-bubble")

            driver = webdriver.Chrome(options=chrome_options)

            # chrome_options.add_argument("--incognito")  # Incognito mode


            # Use a fresh user data directory every run
            user_data_dir = tempfile.mkdtemp()
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

            # Strongly disable password manager and credential service
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_setting_values.popups": 2,
            }
            chrome_options.add_experimental_option("prefs", prefs)

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.implicitly_wait(10)
            logger.info("✅ Chrome driver setup successful")

        except Exception as e:
            logger.error(f"❌ Failed to setup Chrome driver: {e}")
            raise
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element with custom timeout"""
        if timeout is None:
            timeout = self.wait_timeout
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    def wait_for_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        if timeout is None:
            timeout = self.wait_timeout
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not clickable: {locator}")
            raise
    
    def safe_click(self, locator, description="element"):
        """Safely click an element with retry logic"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                element = self.wait_for_clickable(locator)
                element.click()
                logger.info(f"✅ Clicked {description}")
                return True
            except Exception as e:
                logger.warning(f"⚠️  Attempt {attempt + 1} failed to click {description}: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(1)
                else:
                    logger.error(f"❌ Failed to click {description} after {max_attempts} attempts")
                    raise
    
    def safe_type(self, locator, text, description="field", clear_first=True):
        """Safely type text into an element"""
        try:
            element = self.wait_for_element(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"✅ Entered text in {description}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to type in {description}: {e}")
            raise
    
    def navigate_to_site(self):
        """Navigate to the CURA website"""
        try:
            logger.info("🌐 Navigating to CURA Healthcare website...")
            self.driver.get(self.base_url)
            
            # Wait for page to load
            self.wait_for_element((By.TAG_NAME, "body"))
            logger.info("✅ Successfully navigated to website")
            
        except Exception as e:
            logger.error(f"❌ Failed to navigate to website: {e}")
            raise
    
    def login(self, username=None, password=None):
        """Login to the application"""
        try:
            logger.info("🔑 Starting login process...")
            
            # Use provided credentials or default ones
            username = username or self.credentials["username"]
            password = password or self.credentials["password"]
            
            # Navigate to site first
            self.navigate_to_site()
            
            # Click Make Appointment button
            self.safe_click((By.LINK_TEXT, "Make Appointment"), "Make Appointment button")
            
            # Wait for login form
            self.wait_for_element((By.ID, "txt-username"))
            
            # Enter credentials
            self.safe_type((By.ID, "txt-username"), username, "username field")
            self.safe_type((By.ID, "txt-password"), password, "password field")
            
            # Click login button
            self.safe_click((By.ID, "btn-login"), "login button")
            
            # Wait for appointment page to load
            self.wait_for_element((By.ID, "combo_facility"))
            logger.info("✅ Login successful!")
            
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
            self.take_screenshot("login_error.png")
            raise
    
    def make_appointment(self, appointment_config=None):
        """Make an appointment with specified configuration"""
        try:
            logger.info("📅 Starting appointment booking...")
            
            # Default configuration
            default_config = {
                "facility": "Tokyo CURA Healthcare Center",
                "readmission": False,
                "healthcare_program": "Medicare",
                "visit_date": None,
                "comment": "Automated appointment booking via Selenium"
            }
            
            # Use provided config or default
            config = appointment_config or default_config
            
            # Select facility
            facility_dropdown = Select(self.wait_for_element((By.ID, "combo_facility")))
            facility_dropdown.select_by_visible_text(config["facility"])
            logger.info(f"✅ Selected facility: {config['facility']}")
            
            # Handle readmission checkbox
            readmission_checkbox = self.wait_for_element((By.ID, "chk_hospotal_readmission"))
            is_checked = readmission_checkbox.is_selected()
            
            if config["readmission"] and not is_checked:
                readmission_checkbox.click()
                logger.info("✅ Enabled hospital readmission")
            elif not config["readmission"] and is_checked:
                readmission_checkbox.click()
                logger.info("✅ Disabled hospital readmission")
            
            # Select healthcare program
            program_mapping = {
                "Medicare": "radio_program_medicare",
                "Medicaid": "radio_program_medicaid",
                "None": "radio_program_none"
            }
            
            if config["healthcare_program"] in program_mapping:
                program_id = program_mapping[config["healthcare_program"]]
                self.safe_click((By.ID, program_id), f"healthcare program: {config['healthcare_program']}")
            
            # Set visit date
            visit_date = config["visit_date"]
            if visit_date is None:
                # Use tomorrow's date in DD/MM/YYYY format
                visit_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
            
            # Handle date input
            date_field = self.wait_for_element((By.ID, "txt_visit_date"))
            date_field.click()
            
            # Wait a moment for calendar to appear
            time.sleep(0.5)
            
            # Clear and enter date
            date_field.clear()
            date_field.send_keys(visit_date)
            date_field.send_keys(Keys.TAB)  # Tab to close calendar
            logger.info(f"✅ Set visit date: {visit_date}")
            
            # Add comment
            self.safe_type((By.ID, "txt_comment"), config["comment"], "comment field")
            
            # Book appointment
            self.safe_click((By.ID, "btn-book-appointment"), "Book Appointment button")
            
            # Wait for confirmation page
            self.wait_for_element((By.XPATH, "//h2[contains(text(), 'Appointment Confirmation')]"))
            logger.info("🎉 Appointment booking successful!")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Appointment booking failed: {e}")
            self.take_screenshot("appointment_error.png")
            return False
    
    def get_appointment_confirmation(self):
        """Extract appointment confirmation details"""
        try:
            logger.info("📋 Extracting appointment details...")
            
            details = {}
            
            # Extract details from confirmation page
            elements = {
                'facility': 'facility',
                'readmission': 'hospital_readmission',
                'program': 'program',
                'visit_date': 'visit_date',
                'comment': 'comment'
            }
            
            for key, element_id in elements.items():
                try:
                    element = self.wait_for_element((By.ID, element_id), timeout=5)
                    details[key] = element.text.strip()
                except:
                    details[key] = "N/A"
            
            logger.info("✅ Appointment details extracted successfully")
            return details
            
        except Exception as e:
            logger.error(f"❌ Failed to extract appointment details: {e}")
            return None
    
    def take_screenshot(self, filename=None):
        """Take a screenshot with timestamp"""
        try:
            if filename is None:
                filename = f"cura_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            self.driver.save_screenshot(filename)
            logger.info(f"📸 Screenshot saved: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"❌ Failed to take screenshot: {e}")
            return None
    
    def logout(self):
        """Logout from the application"""
        try:
            self.dismiss_password_popup()
            # Click the menu toggle before logout
            self.safe_click((By.XPATH, '//*[@id="menu-toggle"]'), "menu toggle")
            self.safe_click((By.LINK_TEXT, "Logout"), "logout link")
            logger.info("✅ Logout successful")
        except Exception as e:
            logger.error(f"❌ Logout failed: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("✅ Browser closed successfully")
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")
    
    def run_full_automation(self, appointment_config=None):
        """Run the complete automation workflow"""
        try:
            logger.info("🚀 Starting full automation workflow...")
            
            # Setup
            self.setup_driver()
            
            # Login
            self.login()
            
            # Make appointment
            if self.make_appointment(appointment_config):
                # Take confirmation screenshot
                self.take_screenshot("appointment_confirmation.png")
                
                # Get details
                details = self.get_appointment_confirmation()
                
                if details:
                    logger.info("📋 Appointment Details:")
                    for key, value in details.items():
                        logger.info(f"   {key.upper()}: {value}")
                
                # Wait to see result
                time.sleep(2)
                
                # Logout
                self.logout()
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Full automation failed: {e}")
            self.take_screenshot("automation_error.png")
            return False
            
        finally:
            self.cleanup()

    def dismiss_password_popup(self):
        """Try to dismiss Google password warning popup if present."""
        try:
            # Wait for the popup and click OK if it appears
            popup_ok = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='OK']"))
            )
            popup_ok.click()
            logger.info("✅ Dismissed password warning popup")
        except Exception:
            pass  # Popup not present, ignore

def main():
    """Main function with example usage"""
    # Create bot instance
    bot = CURAAppointmentBot(headless=False)
    
    # Custom appointment configuration
    appointment_config = {
        "facility": "Seoul CURA Healthcare Center",
        "readmission": True,
        "healthcare_program": "Medicaid",
        "visit_date": "25/07/2025",
        "comment": "Follow-up appointment for check-up"
    }
    
    # Run automation
    success = bot.run_full_automation(appointment_config)
    
    if success:
        print("\n🎉 Automation completed successfully!")
    else:
        print("\n❌ Automation failed. Check logs for details.")

if __name__ == "__main__":
    main()