# This is a script to refresh web based Kiosk App (Edge in kiosk mode with power apps application)
# Event listener for the mouse clicks will reset the global timer every click
# When global timer expires Selenium is to refresh the webpage
# ver 0.0.2
# Script by Val

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pynput.mouse import Listener
import time
from threading import Timer
from selenium import webdriver
import json

from selenium.webdriver.edge.options import Options
from time import strftime, localtime
import logging

# This function will be called when any key of the mouse is pressed
class App():
    """
    This is a script to refresh web based Kiosk App
    1) Load JSON config
    2) Launch thread and listen for mouse button clicks
    3) Refresh web page if max_delay expires (no user input for a max_delay of time)
    """
    def __init__(self):
        self.start_time = time.time()
        self.setup_logging()
        # Configure web driver - MS Edge
        self.edge_options = Options()
        self.edge_options.add_argument("--kiosk")
        self.edge_options.add_argument("disable-infobars")
        self.edge_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Edge(options=self.edge_options)

    def setup_logging(self):
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='debug.log',
                            filemode='w')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger().addHandler(console)
        # define loggers for other areas in application
        self.logger1 = logging.getLogger("myApp.web_refresher_timer")
        self.logger2 = logging.getLogger("myApp.load_json")
    def on_click(self, *args):
        """
        This function listens for Left Mouse Click (LMB)
        and calls web_refre
        :param args:
        :return:
        """
        logging.info(f"Check which argument was passed: {args}")
        if args[-1]:
            # start timer when the mouse key is pressed
            logging.info('The "{}" mouse key has held down'.format(args[-2].name))
            self.start_time = time.time()
            logging.info(f"Time stamp when LMB click {self.start_time}")

        elif not args[-1]:
            # do nothing
            logging.info('The "{}" mouse key has released'.format(args[-2].name))

    def web_refresh_timer(self, *args):
        """
        This function claculates time elapsed between
        last mouse click and the current time
        When elapsed time is greater than 15 minutes it will
        trigger selenium refresh driver
        :return:
        """
        print("web_refresher_timer function called")
        #global start_time
        print(f"First click at {strftime('%Y-%m-%d %H:%M:%S', localtime(self.start_time))}")
        # Execute this function every 5 seconds
        Timer(5, self.web_refresh_timer).start()
        time_elapsed = time.time() - self.start_time
        print(f"Time elapsed between mouse clicks is: {time_elapsed} (seconds) / {self.max_delay} (seconds)")

        if time_elapsed > self.max_delay:
            self.logger1.warning(f"elapsed time {time_elapsed} more than {self.max_delay} seconds")
            self.start_time = time.time()
            self.logger1.info(f"Reset start time to current time {self.start_time}")

            self.driver.refresh()
            self.logger1.info("Selenium web page - refreshed")

    def load_json(self, *args):
        # Opening JSON file
        try:
            self.logger2.info("Opening JSON config file")
            f = open('config.json')
            # Return JSON object as a dictionary
            data = json.load(f)
            logging.info(data)
            self.max_delay = data.get("refresh_delay")
            self.web_page = data.get("web_page")
            self.driver.get(self.web_page)

            # Closing JSON file
            f.close()

        except FileNotFoundError:
            self.logger2.error("JSON file not found")

    def time_convert(self, sec):
        """
        Not used
        :param sec:
        :return:
        """
        mins = sec // 60
        sec = sec % 60
        hours = mins % 60
        mins = mins % 60
        print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))


"""
Open Listener for mouse click
"""
myApp = App()
with Listener(on_click=myApp.on_click) as Listener:
    #Listen to mouse click
    logging.info("LMB listener activated - Val ver 0.0.2")
    # Load refresh parameters ( delay & webpage)
    myApp.load_json()
    # Call refresher function ( executes every 5 seconds)
    logging.info(f"calling web_refresher_timer()")
    myApp.web_refresh_timer()
    Listener.join()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')
    myApp = App()
    myApp.load_json()
    myApp.on_click()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
