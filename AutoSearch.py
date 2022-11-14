from random import choice
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def search(browser: webdriver, field: str):
    # Find the search box
    sleep(1)
    search_box = WebDriverWait(browser, 5).until(lambda x: x.find_element(By.NAME, 'q'))
    search_box.clear()
    search_box.send_keys(field + Keys.RETURN)
    WebDriverWait(browser, 5).until(lambda x: x.find_element(By.ID, "b_results"))
    sleep(1)


def start(browser: webdriver):
    littre = []
    for line in open("littre.txt", "r"):
        line = line.replace("\n", "")
        littre.append(line)

    # Intensive search, 1 each 2 seconds
    # 35 in total, to ensure that all the points are collected
    for i in range(35):
        try:
            search(browser, choice(littre).lower())
        except Exception as ex:
            print("An error occurred: {}".format(ex))
            print("Closing program in 5 seconds...")
            sleep(5)
            raise

