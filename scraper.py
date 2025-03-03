from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def get_links_selenium(url):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Firefox(options=options)
    
    driver.get(url)
    elements = driver.find_elements(By.TAG_NAME, 'a')
    
    links = {elem.get_attribute('href') for elem in elements if elem.get_attribute('href')}
    
    driver.quit()
    return links

driver = webdriver.Firefox()
driver.get("https://mycourses.rit.edu/d2l/home")

WebDriverWait(driver, 2)
if driver.current_url != "https://mycourses.rit.edu/d2l/home":
    driver.get("https://mycourses.rit.edu/d2l/lp/auth/saml/initiate-login?entityId=https://shibboleth.main.ad.rit.edu/idp/shibboleth&target=%2fd2l%2fhome")
    driver.find_element(By.ID, "ritUsername").send_keys(input("Username: "))
    driver.find_element(By.ID, "ritPassword").send_keys(input("Password: "))
    # WebDriverWait(driver, 10).until(lambda : driver.current_url == "https://mycourses.rit.edu/d2l/home")

print("logged in")