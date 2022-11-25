import logging
import os
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def save_to_desktop(rewards: list):
    """
    Writes all the unvalidated rewards inside a text file placed on the user's Desktop
    :param rewards: List of strings containing all the not validated rewards
    """
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    with open(desktop + "/NotValidatedRewards" + datetime.today().strftime('%d%m%Y') + ".txt", 'w') as file:
        file.writelines(rewards)
        file.close()


def validate_reward(browser: webdriver, points: str, panel, title: str) -> str:
    """
    This function validates rewards corresponding to their category
    :param browser: The WebDriver/browser instance to use
    :param points: The number of points of this reward
    :param panel: The panel containing the reward information
    :param title: The title of the reward
    :return: Returns a reward that wasn't validated, if any
    """
    # Xbox stuff
    if points == "5":
        logging.info("The following reward has been validated:\n\tXBOX REWARD:" + title)
        panel.click()

    # Classic reward:
    if points == "10" and "sondage" not in title.lower():
        logging.info("The following reward has been validated:\n\tCLASSIC REWARD:" + title)
        panel.click()

    # 2 answers survey:
    elif points == "10" and "sondage" in title.lower():
        logging.info("The following reward is under validation:\n\tSURVEY:" + title)
        panel.click()
        sleep(4)
        # Start poll, switch to the new window in order to interact with it
        browser.switch_to.window(browser.window_handles[-1])
        WebDriverWait(browser, 5).until(lambda x: x.find_element(By.ID, "btoption1")).click()

    # 30-points quiz:
    elif points == "30" and "quiz" in title.lower():
        logging.info("The following reward is under validation:\n\tQUIZ:" + title)
        panel.click()
        sleep(4)
        # Start quizz, switch to the new window in order to interact with it
        browser.switch_to.window(browser.window_handles[-1])
        # browser.switch_to.default_content()
        try:
            WebDriverWait(browser, 5).until(lambda x: x.find_element(By.XPATH, "//input[@id='rqStartQuiz']")).click()
            sleep(4)
        except TimeoutException as e:
            logging.warning("Maybe the quiz had already been started? Because the following error was raised:\n{}".
                            format(e))

        # 8 answers-5 correct
        if "expresso" not in title.lower():
            can_continue = True
            while can_continue:
                try:
                    answer = WebDriverWait(browser, 5). \
                        until(
                        lambda x: x.find_element(By.XPATH, "//div[@iscorrectoption='True']//div[@class='b_hide']"))
                    answer.find_element(By.XPATH, "ancestor::div[@iscorrectoption='True']").click()
                    sleep(4)
                except TimeoutException:
                    can_continue = False

        # 4 answers-1 correct
        else:
            can_continue = True
            while can_continue:
                try:
                    for i in range(4):
                        # Works, even if the first answer is the correct one
                        WebDriverWait(browser, 5).until(
                            lambda x: x.find_element(By.ID, "rqAnswerOption{}".format(i))).click()
                        sleep(4)
                except TimeoutException:
                    can_continue = False

    # 50 points true/false quiz -> Human only
    elif points == "50/50" and "quiz" in title.lower():
        logging.warning("The script was unable to validate this reward:\n\tTRUE/FALSE:" + title)
        return "TRUE/FALSE:" + title

    # Others unknown types of rewards, unsupported
    else:
        logging.warning("The script was unable to validate this reward:\n\tUNKNOWN:" + title)
        return "UNKNOWN:" + title

    sleep(4)
    browser.switch_to.window(browser.window_handles[0])
    return ""


def start(browser: webdriver):
    """
    This function performs logic to gather and start rewards validation
    :param browser: The WebDriver/browser instance to use
    """
    missed_rewards = []
    # Find rewards elements using their number of points
    rewards = WebDriverWait(browser, 5).\
        until(lambda x: x.find_elements(By.XPATH, "//span[@ng-if='$ctrl.pointsString']"))
    for t in rewards:
        # We find rewards to validate using the little orange-ish 'plus' icon
        if t.find_element(By.XPATH, "parent::div//span[1]").get_attribute("class") == "mee-icon mee-icon-AddMedium":
            points = t.text
            panel = t.find_element(By.XPATH, "ancestor::a")
            title = panel.get_attribute("aria-label")
            r = validate_reward(browser, points, panel, title)
            if r is not None and r != "":
                missed_rewards.append(r + "\n")
    if len(missed_rewards) >= 1:
        save_to_desktop(missed_rewards)
