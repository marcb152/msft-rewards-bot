import logging

import AutoSearch
import BrowserManager
import RewardsValidator


class ThreadingLib:
    """
    This class is used in order to launch Threads easily by passing all the parameters before starting the threads
    """
    def __init__(self, user: str, password: str, use_headless: bool = False, path: str = ""):
        """
        Constructor of the ThreadingLib class
        :param user: Username of the used Microsoft account
        :param password: Password of the used Microsoft account
        :param use_headless: Launches Chrome in the background if True (=invisible)
        :param path: Path to the Google Chrome WebDriver executable
        """
        self.user = user
        self.password = password
        self.use_headless = use_headless
        self.path = path

    def start_mobile(self):
        """
        Function used to perform the logic in order to start mobile searches
        """
        logging.info("=====LOGGING IN (MOBILE)=====")
        with BrowserManager.start_bing(
                self.user, self.password, use_headless=self.use_headless, mobile=True, path=self.path) as browser:
            logging.info("=====AUTO-SEARCH STARTED (MOBILE)=====")
            AutoSearch.start(browser, 25)
            logging.info("=====AUTO-SEARCH ENDED (MOBILE)=====")
            BrowserManager.close_browser(browser)

    def start_rewards(self, double_check: bool = False, write_to_desktop: bool = False):
        """
        Function used to perform the logic in order to start rewards validation
        :param write_to_desktop: Do we write a list of all the rewards that have not been validated
        :param double_check: Argument used to check for rewards twice
        """
        logging.info("=====LOGGING IN=====")
        with BrowserManager.start_bing(
                self.user, self.password, use_headless=self.use_headless, path=self.path) as browser:
            # TODO: handle bad password/bad username
            BrowserManager.goto_rewards(browser)
            logging.info("=====AUTO-REWARDS STARTED=====")
            RewardsValidator.start(browser, write_to_desktop=write_to_desktop)
            logging.info("=====AUTO-REWARDS ENDED=====")
            if double_check:
                BrowserManager.goto_rewards(browser)
                logging.info("=====AUTO-REWARDS STARTED (x2)=====")
                RewardsValidator.start(browser)
                logging.info("=====AUTO-REWARDS ENDED (x2)=====")
            BrowserManager.close_browser(browser)

    def start_desktop(self):
        """
        Function used to perform the logic in order to start desktop searches
        """
        logging.info("=====LOGGING IN=====")
        with BrowserManager.start_bing(
                self.user, self.password, use_headless=self.use_headless, path=self.path) as browser:
            logging.info("=====AUTO-SEARCH STARTED=====")
            AutoSearch.start(browser)
            logging.info("=====AUTO-SEARCH ENDED=====")
            BrowserManager.close_browser(browser)
