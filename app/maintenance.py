#!/usr/bin/env python

# Import Selenium Libraries
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.firefox.service import Service as Firefox_Service
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By

# Import urlencode
from urllib.parse import urlencode

# Python Module to Load .env Files and set Environment Parameters
from dotenv import dotenv_values

# Import pprint
import pprint

# Import os
import os

# Import time
import time

# Main Function
def main(*args):
    # Debug
    print("Load Configuration from .env File")

    # Load .env Environment Parameters
    CONFIG = dotenv_values(".env")

    # Debug
    print("Load further Configuration from Environment Variables")

    APT_CACHER_NG_HOSTNAME = os.getenv("APT_CACHER_NG_HOSTNAME")
    APT_CACHER_NG_PORT = os.getenv("APT_CACHER_NG_PORT")
    APT_CACHER_NG_PROTOCOL = os.getenv("APT_CACHER_NG_PROTOCOL")
    APT_CACHER_NG_ADMIN_USERNAME = os.getenv("APT_CACHER_NG_ADMIN_USERNAME")
    APT_CACHER_NG_ADMIN_PASSWORD = os.getenv("APT_CACHER_NG_ADMIN_PASSWORD")

    # Define Base URL
    if APT_CACHER_NG_ADMIN_USERNAME is not None and APT_CACHER_NG_ADMIN_PASSWORD is not None:
        base_url = f"{APT_CACHER_NG_PROTOCOL}://{APT_CACHER_NG_ADMIN_USERNAME}:{APT_CACHER_NG_ADMIN_PASSWORD}@{APT_CACHER_NG_HOSTNAME}:{APT_CACHER_NG_PORT}/acng-report.html"
    else:
        base_url = f"{APT_CACHER_NG_PROTOCOL}://{APT_CACHER_NG_HOSTNAME}:{APT_CACHER_NG_PORT}/acng-report.html"

    # Define Query Parameters
    params = dict()
    params["ignoreTradeOff"] = "iTO"
    params["byPath"] = "bP"
    params["byChecksum"] = "bS"
    params["truncNow"] = "tN"
    params["incomAsDamaged"] = "iad"
    params["purgeNow"] = "pN"
    params["doExpire"] = "Start+Scan+and%2For+Expiration"
    params["calcSize"] = "cs"
    params["asNeeded"] = "an"

    # Anchor
    anchor_name = "bottom"

    # Encode Parameters
    params_encoded = urlencode(params)

    # Build overall URL
    url = f"{base_url}?{params_encoded}#{anchor_name}"

    # Print
    print(f"Perform GET Request to URL: {url}")

    # Configure Browser Options
    options = Firefox_Options()
    #options.add_argument("--headless")
    options.add_argument("-headless")
    #options.headless = True

    # Debug
    # print(options)

    # Configure Firefox Service
    # service = Firefox_Service(executable_path=GeckoDriverManager().install())
    # service = Firefox_Service()

    # Configure Browser Binary
    # binary = FirefoxBinary("/opt/firefox/default/firefox-bin")
    # options.binary_location = "/opt/firefox/default/firefox"

    # Other Option / Ideas
    # firefox_bin = "/snap/firefox/current/usr/lib/firefox/firefox"
    # firefoxdriver_bin = "/snap/firefox/current/usr/lib/firefox/geckodriver"
    # options = selenium.webdriver.firefox.options.Options()
    # options.binary_location = firefox_bin
    # service = selenium.webdriver.firefox.service.Service(executable_path=firefoxdriver_bin, service_args=['--log', 'debug'], log_output="gecko.log")
    # browser = selenium.webdriver.Firefox(service=service, options=options)

    # Initialize Selenium Webdriver
    # driver = webdriver.Firefox(service=service, options=options, firefox_binary=binary)
    # driver = webdriver.Firefox(service=service, options=options)
    driver = webdriver.Firefox(options=options)

    # Maximize Window
    # driver.maximize_window()

    # Perform GET Request
    driver.get(url)

    # Get Page Source
    page_source = driver.page_source

    # Get Log
    log_data_start = driver.find_element(By.ID, "logArea").text

    # Debug
    print("Response from apt-cacher-ng at the Beginning of the Maintenance")
    print(log_data_start)

    # Save to Log
    # ...

    # Get Blob
    # <input type="hidden" name="blob" value="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX">

    # Execute Javascript Function to select all Items
    # <button type="button" onclick="checkOrUncheck(true);">Check all</button>
    driver.execute_script("checkOrUncheck(true);")

    # Perform Delete Action
    # <input type="submit" name="doDelete" value="Delete selected files">
    button_doDelete = driver.find_element(By.NAME, "doDelete");
    button_doDelete.click();

    # Perform Truncate Action
    # <input type="submit" name="doTruncate" value="Truncate selected files to zero size">
    # button_doTruncate = driver.findElement(By.NAME, "doTruncate");
    # button_doTruncate.click();

    # Confirm Action (Delete)
    # <input type="submit" name="doDeleteYes" value="Delete now">

    # Confirm Action (Truncate)
    # <input type="submit" name="doTruncateYes" value="Truncate now">

    # Pause to observe the Results
    # time.sleep(300)

    # Get Log
    log_data_end = driver.find_element(By.ID, "logArea").text

    # Debug
    print("Intermediate Response from apt-cacher-ng after Deletion Request")
    print(log_data_end)

    # Confirm Action (Delete)
    button_doDelete_confirm = driver.find_element(By.NAME, "doDeleteYes");
    button_doDelete_confirm.click();

    # Confirm Action (Truncate)
    # button_doTruncate_confirm = driver.findElement(By.NAME, "doTruncateYes");
    # button_doTruncate_confirm.click();

    # Get Log
    log_data_confirmed = driver.find_element(By.ID, "logArea").text

    # Debug
    print("Response from apt-cacher-ng after Deletion Confirmation")
    print(log_data_confirmed)

    # Quit
    driver.quit()

# Main Function (Execution as Script)
if __name__ == "__main__":
    # Run Main Function
    main()
