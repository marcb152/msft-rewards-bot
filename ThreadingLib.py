import logging

import AutoSearch
import BrowserManager
import RewardsValidator


class ThreadingLib:
    def __init__(self, user: str, password: str, use_headless: bool):
        self.user = user
        self.password = password
        self.use_headless = use_headless

    def start_mobile(self):
        logging.info("=====LOGGING IN (MOBILE)=====")
        with BrowserManager.start_bing(self.user, self.password, use_headless=self.use_headless, mobile=True) as browser:
            logging.info("=====AUTO-SEARCH STARTED (MOBILE)=====")
            AutoSearch.start(browser, 25)
            logging.info("=====AUTO-SEARCH ENDED (MOBILE)=====")
            BrowserManager.close_browser(browser)
            return

    def start_rewards(self, double_check: bool = False):
        logging.info("=====LOGGING IN=====")
        with BrowserManager.start_bing(self.user, self.password, use_headless=self.use_headless) as browser:
            # TODO: handle bad password/bad username
            BrowserManager.goto_rewards(browser)
            logging.info("=====AUTO-REWARDS STARTED=====")
            RewardsValidator.start(browser)
            logging.info("=====AUTO-REWARDS ENDED=====")
            if double_check:
                BrowserManager.goto_rewards(browser)
                logging.info("=====AUTO-REWARDS STARTED (x2)=====")
                RewardsValidator.start(browser)
                logging.info("=====AUTO-REWARDS ENDED (x2)=====")
            BrowserManager.close_browser(browser)
            return

    def start_desktop(self):
        logging.info("=====LOGGING IN=====")
        with BrowserManager.start_bing(self.user, self.password, use_headless=self.use_headless) as browser:
            logging.info("=====AUTO-SEARCH STARTED=====")
            AutoSearch.start(browser)
            logging.info("=====AUTO-SEARCH ENDED=====")
            BrowserManager.close_browser(browser)
            return
