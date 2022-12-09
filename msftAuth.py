import logging
import threading
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def login(browser: webdriver, username: str, password: str, e: threading.Event, code: list) -> webdriver:
    """
    This function logins the user to bing using a Microsoft account
    DISCLAIMER: This code won't crash if the password is incorrect, your rewards and searches won't be validated
    :param browser: The WebDriver/browser instance to log in onto
    :param username: Username of the used Microsoft account
    :param password: Password of the used Microsoft account
    :param e: Event fired if 2FA is detected as enabled
    :param code: The 2FA code to log in into the accounts
    :return: Returns the connected WebDriver/browser instance
    """
    # Logout
    browser.get("https://rewards.bing.com/Signout")
    sleep(1)
    WebDriverWait(browser, 5).until(lambda x: "bienvenue" in x.title.lower())
    browser.get("https://login.live.com/login.srf?wa=wsignin1.0&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx&wp=MBI_SSL")
    sleep(1)
    WebDriverWait(browser, 5).until(lambda x: "connecter" in x.title.lower())

    # Authenticate using provided username and password
    try:
        username_field = WebDriverWait(browser, 5).until(lambda x: x.find_element(By.XPATH, "//input[@name='loginfmt']"))
        username_field.send_keys(username + Keys.RETURN)
        sleep(1)
        password_field = WebDriverWait(browser, 5).until(lambda x: x.find_element(By.XPATH, "//input[@name='passwd']"))
        password_field.send_keys(password + Keys.RETURN)
        sleep(1)
    except Exception as e:
        raise Exception("Failed to perform login correctly, maybe there is a typo in your username or password?") from e

    # Incorrect password detection
    try:
        WebDriverWait(browser, 5).until_not(lambda x: x.find_element(By.ID, "passwordError"))
    except TimeoutException:
        raise Exception("Incorrect password! Please restart the script and provide a correct password.")

    # 2FA detection is enabled on the account:
    try:
        _2FA_field = WebDriverWait(browser, 5).until(lambda x: x.find_element(By.ID, "idTxtBx_SAOTCC_OTC"))
        if not e.is_set():
            e.set()
        # Wait for the main thread to reply back
        timeout = 0
        while len(code) == 0 and timeout <= 30:
            sleep(1)
            timeout += 1
        logging.info("2FA code received!")
        _2FA_field.send_keys(code[0] + Keys.RETURN)
    except TimeoutException:
        logging.info("2FA not enabled")

    WebDriverWait(browser, 5).until(lambda x: "compte microsoft" in x.title.lower())
    # Validating "stay connected? -> NO"
    try:
        WebDriverWait(browser, 5).until(lambda x: x.find_element(By.ID, "idBtn_Back")).click()
    except TimeoutException:
        logging.info("No validation required")
    sleep(1)
    WebDriverWait(browser, 5).until(lambda x: "bing" in x.title.lower())

    return browser

