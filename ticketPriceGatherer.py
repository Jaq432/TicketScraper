import time
from selenium import webdriver
import csv
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup
#import pyautogui

# Flag for testing
testing = False

def extract_cost_quantities(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    pattern = r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?'
    costs = re.findall(pattern, soup.get_text())
    return costs


def emailValues(fileName):
    browser.get("https://outlook.live.com/owa/?nlp=1")

    time.sleep(5)  # Wait for the page to load

    pyautogui.typewrite('email')
    pyautogui.press('enter')

    # Wait for the password page to load
    time.sleep(5)

    pyautogui.typewrite('password')
    pyautogui.press('enter')

    # Wait for the page to load
    time.sleep(10)

    # Press enter again due to a login check
    pyautogui.press('enter')

    time.sleep(20)

    # Start a new email
    pyautogui.press('n')

    time.sleep(20)

    # Fill in the email address
    pyautogui.typewrite('Jaq432')
    time.sleep(2)
    pyautogui.press('tab')
    time.sleep(2)
    pyautogui.press('tab')
    time.sleep(2)
    pyautogui.typewrite('Current Ticket Prices')
    time.sleep(2)
    pyautogui.press('tab')
    time.sleep(2)

    dataFile = open(str(fileName), "r")

    for line in dataFile:
        pyautogui.typewrite(str(line))
                
    time.sleep(10)

    dataFile.close()

    # Send the email
    pyautogui.hotkey('ctrl', 'enter')

    time.sleep(5)


def waitBetweenRuns(minutes):
    # Execute it every x minutes
    if minutes == 0:
        return
    
    # Every minute print off the remaining minutes
    for i in range(minutes):
        print("Waiting " + str(minutes - i) + " minutes to run again.")
        time.sleep(60)


# Keep it running
while True:

    # Delete the pageSource.txt file if it exists
    #if os.path.exists("pageSource.txt"):
    #    os.remove("pageSource.txt")

    # Delete the dollar_strings.csv file if it exists
    #if os.path.exists("dollar_strings.csv"):
    #    os.remove("dollar_strings.csv")

    # Define a dictionary to map URLs to their corresponding aliases
    url_aliases = {"https://www.stubhub.com/taylor-swift-denver-tickets-7-14-2023/event/151214616/?quantity=2":"Friday on Stubhub",
                    "https://www.stubhub.com/taylor-swift-denver-tickets-7-15-2023/event/150593672/?quantity=2":"Saturday on Stubhub",
                    "https://www.tickpick.com/buy-taylor-swift-muna-gracie-abrams-tickets-empower-field-at-mile-high-7-14-23-6pm/5427632/?qty=2-false&sortType=P":"Friday on TickPick",
                    "https://www.tickpick.com/buy-taylor-swift-muna-gracie-abrams-tickets-empower-field-at-mile-high-7-15-23-6pm/5406734/?qty=2-false&sortType=P":"Saturday on TickPick",}

    # List of URLs to load
    urls = ["https://www.stubhub.com/taylor-swift-denver-tickets-7-14-2023/event/151214616/?quantity=2",
            "https://www.stubhub.com/taylor-swift-denver-tickets-7-15-2023/event/150593672/?quantity=2",
            "https://www.tickpick.com/buy-taylor-swift-muna-gracie-abrams-tickets-empower-field-at-mile-high-7-14-23-6pm/5427632/?qty=2-false&sortType=P",
            "https://www.tickpick.com/buy-taylor-swift-muna-gracie-abrams-tickets-empower-field-at-mile-high-7-15-23-6pm/5406734/?qty=2-false&sortType=P"]

    # Initialize the Chrome browser
    browser = webdriver.Chrome()

    currentTime = datetime.now()
    timestamp = currentTime.strftime("%Y_%m_%d_%H_%M_%S")

    # Loop through each URL
    for url in urls:
        # Load the URL
        browser.get(url)

        # Wait for 10 seconds for the page to load
        time.sleep(10)

        # Flag for TickPick filter
        tickPickFilterFlag = False
        wasTickPickUrl = False
        tickPickPageSource = ""

        # Get the page source
        pageSource = browser.page_source

        # Save the page source to a text file
        with open("pageSource.txt", "w", encoding="utf-8") as f:
            f.write(pageSource)

        # Remove the tickpick filtered page source if it exists
        if os.path.exists("tickPickPageSource.txt"):
            os.remove("tickPickPageSource.txt")

        # Go through the page source and look for tickpick
        # If it is, we want to filter the selection so we only look at ticket prices
        with open("pageSource.txt", "r", encoding="utf-8") as j:
            for line in j:
                with open("tickPickPageSource.txt", "a", encoding="utf-8") as h:
                    if '<div id="listingsInner" class="inner customSlide">' in line:
                        # Here we want to apply the search
                        tickPickFilterFlag = True
                        wasTickPickUrl = True
                    if '<div id="moreListings" class="activeML">' in line:
                        # Here we want to stop the search
                        tickPickFilterFlag = False
                    if tickPickFilterFlag:
                        h.write(line)

        with open("tickPickPageSource.txt", "r", encoding="utf-8") as i:
            for line in i:
                tickPickPageSource += str(line)
        
        # Find all strings with ">$" in the page source and save the next 3 characters to a list
        costStrings = []
        pattern = r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?'

        if wasTickPickUrl:
            for match in re.finditer(pattern, tickPickPageSource):
                #print(match)
                costString = match.group(0)
                costStrings.append(int(costString.replace(",","").replace("$","")))
        else:
            for match in re.finditer(pattern, pageSource):
                #print(match)
                costString = match.group(0)
                costStrings.append(int(costString.replace(",","").replace("$","")))

        # Sort the four character strings in ascending order
        sorted_costStrings = sorted(costStrings)
        
        # Get the alias for the URL
        alias = url_aliases[url]

        # Append the sorted strings and timestamp to a CSV file
        #fileName = "dollar_strings/dollar_strings_" + str(timestamp) + ".csv"
        fileName = "dollar_strings/dollar_strings.csv"
        if not os.path.exists(str(fileName)):
            newDollarStringsFile = open(str(fileName), "w")
        with open(str(fileName), "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for costString in sorted_costStrings:
                writer.writerow([timestamp, alias, costString])

    if testing:
        exit()


    print("Last time of scraping: " + str(timestamp))

    browser.close()

    # Email the values to myself
    #emailValues(fileName)

    print("\nCompleted the scaping.")

    # Build in a break to avoid over-scraping
    waitBetweenRuns(0)





    