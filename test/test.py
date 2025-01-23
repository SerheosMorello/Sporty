import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 ('
                         'KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_twitch_starcraft(driver):
    # 1. Open Twitch
    driver.get("https://www.twitch.tv")

    # Wait until page is loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 2. Click search button
    search_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div[2]/a[2]/div"))
    )
    search_icon.click()

    # 3. Type "StarCraft II" in search input
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))
    )
    search_input.send_keys("StarCraft II")
    search_input.send_keys(Keys.RETURN)

    # 4. Scroll down 2 times
    time.sleep(2)  # We give time for the results to load.
    action = ActionChains(driver)
    for _ in range(2):
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)

    # 5. Choosing the first streamer
    streamer = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/videos/') or contains(@href, '/streams/')]"))
    )
    streamer.click()

    # 6. On the streamer's page, wait for it to load completely and take a screenshot
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//video"))
    )
    time.sleep(3)  # Additional time for full loading
    driver.save_screenshot("streamer_page.png")
    print("Save screenshot: streamer_page.png")
