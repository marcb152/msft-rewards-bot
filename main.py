import logging
import sys

from easygui import passwordbox, enterbox

import AutoSearch
import BrowserManager
import RewardsValidator


def usage(arg_name: str = ""):
    print("Usage:\t" + arg_name + " [--headless] [--double-check]")
    print(" --headless: Launches Edge in the background, its window won't appear")
    print(" --double-check: Will check 2 times for rewards, in case something wasn't correctly validated")
    print("Made with <3 by:\n\t- Marc // PiNutStudio // marcb152")


# TODO: Implement selenium-stealth
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(filemode='w',
                        stream=sys.stdout,
                        level=logging.INFO,
                        force=True,
                        format='%(asctime)s - %(levelname)s: %(module)s: %(message)s [at line %(lineno)d]')

    # TODO: Replace args with the parser package
    use_headless = False
    double_check = False
    match len(sys.argv):
        case 2:
            if sys.argv[1] == "--headless":
                use_headless = True
            elif sys.argv[1] == "--double-check":
                double_check = True
            else:
                usage(sys.argv[1])
        case 3:
            if sys.argv[1] == "--headless" and sys.argv[2] == "--double-check":
                use_headless = True
                double_check = True
            elif sys.argv[2] == "--headless" and sys.argv[1] == "--double-check":
                use_headless = True
                double_check = True
            else:
                usage(sys.argv[1] + " and " + sys.argv[2])
        case default:
            usage()

    user = enterbox("Enter username:", "User auth credentials")
    assert user != "" and user is not None, "The username can't be empty!"
    logging.info("Username OK")

    password = passwordbox("Enter password:", "User auth credentials")
    assert password != "" and password is not None, "The password can't be empty!"
    logging.info("Password OK")

    logging.info("=====LOGGING IN=====")
    with BrowserManager.start_bing(user, password, use_headless) as browser:
        # TODO: handle bad password/bad username
        logging.info("=====AUTO-SEARCH STARTED=====")
        AutoSearch.start(browser)
        logging.info("=====AUTO-SEARCH ENDED=====")
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
