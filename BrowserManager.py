from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth

import msftAuth


def start_chrome(username: str, password: str, use_headless: bool = False, mobile: bool = False, path: str = "") -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    if use_headless:
        options.add_argument("--headless")
    if mobile:
        options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/79.0. 3945.79 Mobile Safari/537.36")
        options.add_experimental_option("mobileEmulation", {"deviceName": "Pixel 3"})
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
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
    return msftAuth.login(browser, username, password)


def start_bing(username: str, password: str, use_headless: bool = False, mobile: bool = False, path: str = "") -> webdriver:
    browser = start_chrome(username, password, use_headless=use_headless, mobile=mobile, path=path)
    browser.get("https://www.bing.com/")
    assert "Bing" in browser.title
    sleep(2)
    # Accept/reject cookies
    WebDriverWait(browser, 5).until(lambda x: x.find_element(By.ID, "bnp_btn_reject")).click()
    sleep(1)
    return browser


def goto_rewards(browser: webdriver) -> webdriver:
    browser.get("https://rewards.bing.com/")
    assert "Rewards" in browser.title
    sleep(2)
    # Accept/reject cookies
    WebDriverWait(browser, 5).until(lambda x: x.find_element(By.XPATH, "//div[@id='wcpConsentBannerCtrl']//button[1]")).click()
    sleep(1)
    return browser


def close_browser(browser: webdriver):
    sleep(1)
    # Deleting cookies
    browser.delete_all_cookies()
    # TODO: Rework clearing cache, not working properly yet
    # sleep(1)
    # Clearing cache
    # browser.get('chrome://settings/clearBrowserData')
    # browser.switch_to.window(browser.window_handles[0])
    # browser.find_element(By.XPATH, '//settings-ui').send_keys(Keys.ENTER)
    sleep(1)
    browser.quit()
