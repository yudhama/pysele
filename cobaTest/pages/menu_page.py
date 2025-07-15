from selenium.webdriver.common.by import By
from .base_page import BasePage

class MenuPage(BasePage):
    MENU_TOGGLE = (By.XPATH, '//*[@id="menu-toggle"]')
    LOGOUT = (By.LINK_TEXT, "Logout")

    def logout(self):
        self.click(self.MENU_TOGGLE)
        self.click(self.LOGOUT)