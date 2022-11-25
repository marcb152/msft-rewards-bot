from random import choice
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def search(browser: webdriver, field: str):
    """
    This function uses Bing to send web searches
    :param browser: The WebDriver/browser to use
    :param field: The field to search for using Bing
    """
    # Find the search box
    sleep(1)
    search_box = WebDriverWait(browser, 5).until(lambda x: x.find_element(By.NAME, 'q'))
    search_box.clear()
    search_box.send_keys(field + Keys.RETURN)
    WebDriverWait(browser, 5).until(lambda x: x.find_element(By.ID, "b_results"))
    sleep(1)


def start(browser: webdriver, searches_nbr: int = 35):
    """
    This function uses random words from a French dictionary to perform automatic web searches on Bing
    :param browser: The WebDriver/browser instance to use
    :param searches_nbr: The number of web searches to perform, default to 35 (desktop), add a few ones for safety
    """
    littre = []
    for line in open("littre.txt", "r"):
        line = line.replace("\n", "")
        littre.append(line)

    # Intensive search, 1 each 2 seconds
    # 35 in total, to ensure that all the points are collected
    for i in range(searches_nbr):
        try:
            search(browser, choice(littre).lower())
        except Exception as e:
            raise Exception("An error occurred during web searches, the program will close itself shortly") from e

