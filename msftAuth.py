import logging
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def login(browser: webdriver, username: str, password: str) -> webdriver:
    # Logout
    browser.get("https://rewards.bing.com/Signout")
    sleep(1)
    WebDriverWait(browser, 5).until(lambda x: "bienvenue" in x.title.lower())
    # Login
    browser.get("https://login.live.com")
    sleep(1)
    WebDriverWait(browser, 5).until(lambda x: "connecter" in x.title.lower())
    # Auth using username and password
    username_field = WebDriverWait(browser, 5).until(lambda x: x.find_element(By.XPATH, "//input[@name='loginfmt']"))
    username_field.send_keys(username + Keys.RETURN)
    sleep(1)
    password_field = WebDriverWait(browser, 5).until(lambda x: x.find_element(By.XPATH, "//input[@name='passwd']"))
    password_field.send_keys(password + Keys.RETURN)
    sleep(1)
    WebDriverWait(browser, 5).until(lambda x: "compte microsoft" in x.title.lower())
    # Validating "stay connected?"
    try:
        WebDriverWait(browser, 5).until(lambda x: x.find_element(By.XPATH, "//input[@type='submit']")).click()
    except:
        logging.info("No validation required")
    sleep(1)
    WebDriverWait(browser, 5).until(lambda x: "compte microsoft" in x.title.lower())

    return browser

