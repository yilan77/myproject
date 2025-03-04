from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

def login(driver):
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

def wait_for_load(driver, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if driver.execute_script("return document.readyState") == "complete":
            return True
        time.sleep(0.1)
    return False

def get_links(url, driver):
    driver.get(url)
    if wait_for_load(driver):
        elements = driver.find_elements(By.TAG_NAME, 'a')
        links = [element.get_attribute('href') for element in elements if element.get_attribute('href')]
        return links
    return []

def crawl_website(start_url, driver, file, max_pages=200):
    """Crawls a website using BFS to avoid recursion errors"""
    queue = [start_url]
    visited = set()
    all_links = []

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        print(f"🔗 Crawling: {url}")
        try:
            links = get_links(url, driver)
            for link in links:
                if link not in visited and link.startswith("https://mycourses.rit.edu"):
                    queue.append(link)
                    all_links.append(link)
                    file.write(link + '\n')
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")

    return all_links

def open_links(driver, filename):
    driver.get('about:config')
    driver.find_element(By.ID, "warningButton").click()
    driver.find_element(By.ID, "about-config-search").send_keys('dom.popup_maximum')
    time.sleep(0.5)
    driver.find_element(By.CLASS_NAME, 'button-edit').click()
    driver.find_element(By.XPATH, '//*[@aria-label="dom.popup_maximum"]').send_keys('2000')
    driver.find_element(By.CLASS_NAME, 'button-save').click()
    with open(filename, 'r') as file:
        for line in file:
            driver.execute_script(f"window.open('{line.strip()}', '_blank')")
            print(line)

# Start WebDriver
driver = webdriver.Firefox()

# Log in
login(driver)

# Start crawling
#with open('links.txt', 'w') as file:
#    links = crawl_website("https://mycourses.rit.edu/d2l/home", driver, file)

open_links(driver, "keep/links.txt")