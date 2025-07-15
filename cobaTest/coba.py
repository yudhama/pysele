import time
from selenium import webdriver

# Set up the WebDriver (assuming Chrome)
driver = webdriver.Firefox()

# Open a web page
driver.get("https://www.example.com")

driver.maximize_window()

# Retrieve and print the title of the page
print(driver.title)

# Just for not let the browser immediate closed
time.sleep(5)

# Close the browser
driver.quit()
