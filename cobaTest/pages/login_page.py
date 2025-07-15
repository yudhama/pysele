from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    MAKE_APPOINTMENT = (By.LINK_TEXT, "Make Appointment")
    USERNAME = (By.ID, "txt-username")
    PASSWORD = (By.ID, "txt-password")
    LOGIN_BTN = (By.ID, "btn-login")

    def go_to_login(self):
        self.click(self.MAKE_APPOINTMENT)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)