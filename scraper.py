from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

driver = webdriver.Firefox()
driver.get("https://mycourses.rit.edu/d2l/lp/auth/saml/initiate-login?entityId=https://shibboleth.main.ad.rit.edu/idp/shibboleth&target=%2fd2l%2fhome")
time.sleep(0.5)

with open(".env") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

driver.find_element(By.ID, "ritUsername").send_keys(os.environ['RIT_USERNAME'])
driver.find_element(By.ID, "ritPassword").send_keys(os.environ['RIT_PASSWORD'])
driver.find_element(By.CLASS_NAME, "btn--login").click()

start_time = time.time()
timeout = 15
while True:
    try:
        button = driver.find_element(By.ID, "dont-trust-browser-button")
        button.click()
    except:
        if time.time() - start_time > timeout:
            break
    time.sleep(0.5)

print("logged in")