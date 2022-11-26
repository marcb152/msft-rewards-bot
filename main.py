import argparse
import datetime
import logging
import socket
import sys
import threading
import time

from easygui import passwordbox, enterbox

import ThreadingLib


def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    (Code from StackOverflow)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False


# TODO: Rework logging in order to authorize only my code to send output (to get rid of all the annoying warnings)
if __name__ == '__main__':
    logging.basicConfig(filemode='w',
                        stream=sys.stdout,
                        level=logging.INFO,
                        force=True,
                        format='%(asctime)s - %(levelname)s: %(module)s (%(threadName)s): %(message)s [at line %(lineno)d]',
                        datefmt="%H:%M:%S")

    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_const", const=True,
                        help="Launches Chrome in the background, its window won't appear.")
    parser.add_argument("--double-check", action="store_const", const=True,
                        help="Will check 2 times for rewards, in case something wasn't correctly validated,"
                             "only if rewards validation is enabled.")
    parser.add_argument("--only-rewards", action="store_const", const=True,
                        help="Will only check for rewards, it won't perform auto-searches.")
    parser.add_argument("--mobile", action="store_const", const=True,
                        help="Will perform all the mobile searches needed, won't perform any reward validation.")
    parser.add_argument("--write-to-desktop", action="store_const", const=True,
                        help="Will create a text file on your Desktop listing all the rewards that have not been validated.")
    parser.add_argument("--path", type=str,
                        help="The path to the Chrome Driver executable.")
    args = vars(parser.parse_args())

    start_time = time.time()

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

    # THREADING
    threads = ThreadingLib.ThreadingLib(user, password, use_headless=args["headless"], path=args["path"])
    mobile_thread = threading.Thread(target=threads.start_mobile, name="MobileThread")
    desktop_thread = threading.Thread(target=threads.start_desktop, name="DesktopThread")
    rewards_thread = threading.Thread(target=threads.start_rewards, name="RewardsThread",
                                      args=(args["double_check"], args["write_to_desktop"],))
    if args["mobile"]:
        logging.info("Starting mobile thread...")
        mobile_thread.start()
    if not args["only_rewards"]:
        logging.info("Starting desktop searches thread...")
        desktop_thread.start()
    logging.info("Starting rewards thread...")
    rewards_thread.start()

    # WAITING FOR THREADING
    if args["mobile"]:
        mobile_thread.join()
    if not args["only_rewards"]:
        desktop_thread.join()
    rewards_thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info("Total elapsed seconds: " + str(elapsed_time) +
                 "\n\tTotal time: " + str(datetime.timedelta(seconds=elapsed_time)))
