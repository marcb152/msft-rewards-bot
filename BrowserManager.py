import threading
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth

import msftAuth


def start_chrome(username: str, password: str, e: threading.Event, code: list, use_headless: bool = False,
                 incognito: bool = False, mobile: bool = False, path: str = "") -> webdriver:
    """
    This function starts a Chrome WebDriver instance connected to Bing
    :param username: Username of the used Microsoft account
    :param password: Password of the used Microsoft account
    :param e: Event fired if 2FA is detected as enabled
    :param code: The 2FA code to log in into the accounts
    :param use_headless: Launches Chrome in the background if True (=invisible)
    :param incognito: Launches Chrome in private mode
    :param mobile: Launches Chrome as mobile Chrome if True
    :param path: Path to the Google Chrome WebDriver executable
    :return: Returns the WebDriver/browser instance newly created and connected to the Microsoft account
    """
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    if incognito:
        options.add_argument("--incognito")
    if use_headless:
        options.add_argument("--headless")
    if mobile:
        options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/79.0. 3945.79 Mobile Safari/537.36")
        options.add_experimental_option("mobileEmulation", {"deviceName": "Pixel 3"})
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    if path is not None and path != "":
        browser = webdriver.Chrome(options=options, executable_path=path)
    else:
        browser = webdriver.Chrome(options=options)
    stealth(browser,
            languages=["fr-FR", "fr"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    sleep(1)
    return msftAuth.login(browser, username, password, e, code)


def start_bing(username: str, password: str, e: threading.Event, code: list, use_headless: bool = False,
               incognito: bool = False, mobile: bool = False, path: str = "") -> webdriver:
    """
    This function starts Chrome, logins the user and goes to bing.com
    :param username: Username of the used Microsoft account
    :param password: Password of the used Microsoft account
    :param e: Event fired if 2FA is detected as enabled
    :param code: The 2FA code to log in into the accounts
    :param use_headless: Launches Chrome in the background if True (=invisible)
    :param incognito: Launches Chrome in private mode
    :param mobile: Launches Chrome as mobile Chrome if True
    :param path: Path to the Google Chrome WebDriver executable
    :return: Returns the WebDriver/browser instance newly created and connected to the Microsoft account
    """
    browser = start_chrome(username, password, e, code, incognito=incognito, use_headless=use_headless, mobile=mobile, path=path)
    browser.get("https://www.bing.com/")
    assert "bing" in browser.title.lower()
    sleep(2)
    # Reject cookies
    WebDriverWait(browser, 5).until(lambda x: x.find_element(By.ID, "bnp_btn_reject")).click()
    sleep(1)
    return browser


def goto_rewards(browser: webdriver) -> webdriver:
    """
    This function goes to the Rewards website and clears cookies
    :param browser: The WebDriver/browser instance to use
    :return: Returns the same WebDriver/browser instance as provided
    """
    browser.get("https://rewards.bing.com/")
    sleep(3)
    assert "Rewards" in browser.title
    sleep(1)
    # Accept/reject cookies
    WebDriverWait(browser, 5).until(
        lambda x: x.find_element(By.XPATH, "//div[@id='wcpConsentBannerCtrl']//button[1]")).click()
    sleep(1)
    return browser


def close_browser(browser: webdriver):
    """
    This function closes the provided WebDriver/browser instance
    :param browser: The WebDriver/browser instance to close
    """
    # Logout, might cause issues to the others running instances
    # browser.get("https://rewards.bing.com/Signout")
    sleep(1)
    # Deleting cookies
    browser.delete_all_cookies()
    # TODO: Rework clearing cache, not working properly yet
    # Clearing cache
    # sleep(1)
    # browser.switch_to.window(browser.window_handles[0])
    # browser.get('chrome://settings/clearBrowserData')
    # WebDriverWait(browser, 1).until(lambda x: x.find_element(By.XPATH, '//settings-ui').send_keys(Keys.ENTER))
    sleep(1)
    browser.quit()
