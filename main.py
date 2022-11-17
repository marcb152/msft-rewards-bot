import argparse
import logging
import socket
import sys

from easygui import passwordbox, enterbox

import AutoSearch
import BrowserManager
import RewardsValidator


def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False


if __name__ == '__main__':
    logging.basicConfig(filemode='w',
                        stream=sys.stdout,
                        level=logging.INFO,
                        force=True,
                        format='%(asctime)s - %(levelname)s: %(module)s: %(message)s [at line %(lineno)d]')

    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_const", const=True,
                        help="Launches Chrome in the background, its window won't appear.")
    parser.add_argument("--double-check", action="store_const", const=True,
                        help="Will check 2 times for rewards, in case something wasn't correctly validated,"
                             "only if rewards validation is enabled.")
    parser.add_argument("--only-rewards", action="store_const", const=True,
                        help="Will only check for rewards, it won't perform auto-searches.")
    parser.add_argument("--mobile-searches", action="store_const", const=True,
                        help="Will perform all the mobile searches needed, won't perform any reward validation.")
    args = vars(parser.parse_args())

    if not check_internet():
        logging.error("No internet connection was detected, "
                      "maybe your internet connection isn't fast enough for this script?")
        raise ConnectionError("Can't connect to the internet")
    else:
        logging.info("Internet connectivity OK")

    user = enterbox("Enter username:", "User auth credentials")
    assert user != "" and user is not None, "The username can't be empty!"
    logging.info("Username OK")

    password = passwordbox("Enter password:", "User auth credentials")
    assert password != "" and password is not None, "The password can't be empty!"
    logging.info("Password OK")

    if args["mobile_searches"]:
        logging.info("=====LOGGING IN (MOBILE)=====")
        with BrowserManager.start_bing(user, password, use_headless=args["headless"], mobile=args["mobile_searches"]) as browser:
            logging.info("=====AUTO-SEARCH STARTED (MOBILE)=====")
            AutoSearch.start(browser, 25)
            logging.info("=====AUTO-SEARCH ENDED (MOBILE)=====")
            BrowserManager.close_browser(browser)

    logging.info("=====LOGGING IN=====")
    with BrowserManager.start_bing(user, password, use_headless=args["headless"]) as browser:
        # TODO: handle bad password/bad username
        if not args["only_rewards"]:
            logging.info("=====AUTO-SEARCH STARTED=====")
            AutoSearch.start(browser)
            logging.info("=====AUTO-SEARCH ENDED=====")
        BrowserManager.goto_rewards(browser)
        logging.info("=====AUTO-REWARDS STARTED=====")
        RewardsValidator.start(browser)
        logging.info("=====AUTO-REWARDS ENDED=====")
        if args["double_check"]:
            BrowserManager.goto_rewards(browser)
            logging.info("=====AUTO-REWARDS STARTED (x2)=====")
            RewardsValidator.start(browser)
            logging.info("=====AUTO-REWARDS ENDED (x2)=====")
        BrowserManager.close_browser(browser)
