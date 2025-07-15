from selenium.webdriver.common.by import By
from .base_page import BasePage

class ConfirmationPage(BasePage):
    CONFIRM_HEADER = (By.XPATH, "//h2[contains(text(), 'Appointment Confirmation')]")
    FACILITY = (By.ID, "facility")
    READMISSION = (By.ID, "hospital_readmission")
    PROGRAM = (By.ID, "program")
    VISIT_DATE = (By.ID, "visit_date")
    COMMENT = (By.ID, "comment")

    def get_details(self):
        self.wait_for_element(self.CONFIRM_HEADER)
        return {
            "facility": self.wait_for_element(self.FACILITY).text,
            "readmission": self.wait_for_element(self.READMISSION).text,
            "program": self.wait_for_element(self.PROGRAM).text,
            "visit_date": self.wait_for_element(self.VISIT_DATE).text,
            "comment": self.wait_for_element(self.COMMENT).text,
        }