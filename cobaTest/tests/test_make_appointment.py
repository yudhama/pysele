from cobaTest.pages.login_page import LoginPage
from cobaTest.pages.appointment_page import AppointmentPage
from cobaTest.pages.confirmation_page import ConfirmationPage
from cobaTest.pages.menu_page import MenuPage
from cobaTest.utils.driver_factory import get_driver

def test_make_appointment():

    driver = get_driver(headless=False)
    driver.get("https://katalon-demo-cura.herokuapp.com/")

    login_page = LoginPage(driver)
    appointment_page = AppointmentPage(driver)
    confirmation_page = ConfirmationPage(driver)
    menu_page = MenuPage(driver)

    login_page.go_to_login()
    login_page.login("John Doe", "ThisIsNotAPassword")

    config = {
        "facility": "Seoul CURA Healthcare Center",
        "readmission": True,
        "healthcare_program": "Medicaid",
        "visit_date": "25/07/2025",
        "comment": "Follow-up appointment for check-up"
    }
    appointment_page.book_appointment(config)
    details = confirmation_page.get_details()
    print(details)
    menu_page.logout()
    driver.quit()

if __name__ == "__main__":
    test_make_appointment()