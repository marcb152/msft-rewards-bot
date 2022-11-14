from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait

import msftAuth


def start_edge(username: str, password: str, use_headless: bool = False) -> webdriver:
    edge_options = Options()
    if use_headless:
        edge_options.add_argument("--headless")
    # edge_options.add_argument("-inprivate")
    browser = webdriver.Edge(options=edge_options)
    return msftAuth.login(browser, username, password)


def start_bing(username: str, password: str, use_headless: bool = False) -> webdriver:
    browser = start_edge(username, password, use_headless)
    browser.get("https://www.bing.com/")
    assert "Bing" in browser.title
    browser.maximize_window()
    sleep(2)
    # Accept/reject cookies
    WebDriverWait(browser, 5).until(lambda x: x.find_element(By.ID, "bnp_btn_reject")).click()
    sleep(1)
    return browser


def goto_rewards(browser: webdriver) -> webdriver:
    browser.get("https://rewards.microsoft.com/")
    assert "Rewards" in browser.title
    browser.maximize_window()
    sleep(2)
    # Accept/reject cookies
    WebDriverWait(browser, 5).until(lambda x: x.find_element(By.XPATH, "//div[@id='wcpConsentBannerCtrl']//button[1]")).click()
    sleep(1)
    return browser


def close_browser(browser: webdriver):
    sleep(1)
    browser.delete_all_cookies()
    sleep(1)
    browser.quit()
