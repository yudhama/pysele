from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage

class AppointmentPage(BasePage):
    FACILITY = (By.ID, "combo_facility")
    READMISSION = (By.ID, "chk_hospotal_readmission")
    PROGRAM_MEDICARE = (By.ID, "radio_program_medicare")
    PROGRAM_MEDICAID = (By.ID, "radio_program_medicaid")
    PROGRAM_NONE = (By.ID, "radio_program_none")
    VISIT_DATE = (By.ID, "txt_visit_date")
    COMMENT = (By.ID, "txt_comment")
    BOOK_BTN = (By.ID, "btn-book-appointment")

    def book_appointment(self, config):
        Select(self.wait_for_element(self.FACILITY)).select_by_visible_text(config["facility"])
        readmission = self.wait_for_element(self.READMISSION)
        if config["readmission"] != readmission.is_selected():
            readmission.click()
        program_map = {
            "Medicare": self.PROGRAM_MEDICARE,
            "Medicaid": self.PROGRAM_MEDICAID,
            "None": self.PROGRAM_NONE
        }
        self.click(program_map[config["healthcare_program"]])
        self.type(self.VISIT_DATE, config["visit_date"])
        self.type(self.COMMENT, config["comment"])
        self.click(self.BOOK_BTN)