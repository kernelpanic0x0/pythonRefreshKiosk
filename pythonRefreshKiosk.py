# This is a script to refresh web based Kiosk App (Chrome in kisok mode with power apps application)
# Event listener for the mouse clicks will reset the global timer every click
# When global timer expires Selenium is to refresh the webpage
# ver 0.0.1
# written by Val

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pynput.mouse import Listener
import time
from threading import Timer
from selenium import webdriver

from selenium.webdriver.edge.options import Options


# Configure web driver - MS Edge
edge_options = Options()
edge_options.add_argument("--kiosk")

driver = webdriver.Edge(edge_options=edge_options)
driver.get("https://google.com")

#Global variable
start_time = 0

# This function will be called when any key of the mouse is pressed
def on_click(*args):
    """
    This function listens for Left Mouse Click (LMB)
    and calls web_refre
    :param args:
    :return:
    """
    print(f"Check which argument was passed: {args}")
    if args[-1]:
        # start timer when the mouse key is pressed
        print('The "{}" mouse key has held down'.format(args[-2].name))
        global start_time
        start_time = time.time()
        print(f"Time stamp when LMB click {start_time}")

    elif not args[-1]:
        # do nothing
        print('The "{}" mouse key has released'.format(args[-2].name))

def web_refresh_timer():
    """
    This function claculates time elapsed between
    last mouse click and the current time
    When elapsed time is greater than 15 minutes it will
    trigger selenium refresh driver
    :return:
    """
    print("web_refresher_timer function called")
    global start_time
    print(f"First click at {start_time}")
    # Execute this function every 5 seconds
    Timer(5, web_refresh_timer).start()
    time_elapsed = time.time() - start_time
    print(f"Time elapsed between mouse clicks is: {time_elapsed} (seconds)")

    if time_elapsed > 1800:
        print(f"elapsed time {time_elapsed} more than 1800 seconds (30 minutes")
        start_time = time.time()
        print(f"Reset start time to current time {start_time}")

        driver.refresh()
        print("Selenium web page - refreshed")



"""
Open Listener for mouse click
"""
with Listener(on_click=on_click) as Listener:

    #Listen to mouse click
    print("LMB listener activated - Val ver 0.0.1")
    print(f"calling web_refresher_timer()")
    web_refresh_timer()
    Listener.join()


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins % 60
    mins = mins % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    on_click()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
