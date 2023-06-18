import time
from selenium import webdriver
import csv
import re
import os
from datetime import datetime
import pyautogui

# Keep it running
while True:

    # Delete the page_source.txt file if it exists
    if os.path.exists("page_source.txt"):
        os.remove("page_source.txt")

    # Delete the dollar_strings.csv file if it exists
    if os.path.exists("dollar_strings.csv"):
        os.remove("dollar_strings.csv")

    # Define a dictionary to map URLs to their corresponding aliases
    url_aliases = {"https://www.stubhub.com/taylor-swift-mexico-d-f-tickets-8-24-2023/event/151857905/?quantity=2":"Thursday",
                    "https://www.stubhub.com/taylor-swift-mexico-d-f-tickets-8-25-2023/event/151857932/?quantity=2":"Friday",
                    "https://www.stubhub.com/taylor-swift-mexico-d-f-tickets-8-26-2023/event/151857946/?quantity=2":"Saturday",
                    "https://www.stubhub.com/taylor-swift-mexico-d-f-tickets-8-27-2023/event/151905689/?quantity=2":"Sunday"}

    # List of URLs to load
    urls = ["https://www.stubhub.com/taylor-swift-mexico-d-f-tickets-8-24-2023/event/151857905/?quantity=2",
            "https://www.stubhub.com/taylor-swift-mexico-d-f-tickets-8-25-2023/event/151857932/?quantity=2",
            "https://www.stubhub.com/taylor-swift-mexico-d-f-tickets-8-26-2023/event/151857946/?quantity=2",
            "https://www.stubhub.com/taylor-swift-mexico-d-f-tickets-8-27-2023/event/151905689/?quantity=2"]

    # Initialize the Chrome browser
    browser = webdriver.Chrome()

    # Loop through each URL
    for url in urls:
        # Load the URL
        browser.get(url)

        # Wait for 10 seconds for the page to load
        time.sleep(5)

        # Get the page source
        page_source = browser.page_source

        # Save the page source to a text file
        with open("page_source.txt", "a", encoding="utf-8") as f:
            f.write(page_source)

        # Find all strings with ">$" in the page source and save the next 3 characters to a list
        three_char_strings = []
        pattern = r'">\$[a-zA-Z0-9]{3}'
        for match in re.finditer(pattern, page_source):
            three_char_string = match.group(0)[3:6]
            three_char_strings.append(three_char_string)

        # Sort the three character strings in ascending order
        sorted_three_char_strings = sorted(three_char_strings)

        # Get the current date and time as a formatted string
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Get the alias for the URL
        alias = url_aliases[url]

        # Append the sorted three character strings and timestamp to a CSV file
        with open("dollar_strings.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for three_char_string in sorted_three_char_strings:
                writer.writerow([timestamp, alias, three_char_string])

    # Email the values to myself
    # Open outlook
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
    pyautogui.typewrite('Current Foro Sol Ticket Prices')
    time.sleep(2)
    pyautogui.press('tab')
    time.sleep(2)

    dataFile = open("dollar_strings.csv", "r")

    for line in dataFile:
        pyautogui.typewrite(str(line))
                
    time.sleep(10)

    dataFile.close()

    # Send the email
    pyautogui.hotkey('ctrl', 'enter')

    time.sleep(5)

    # Close the browser
    browser.quit()

    print("Completed the scaping.")

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    print("Last time of scraping: " + str(timestamp))

    # Execute it every x*10 minutes
    numOfTenMin = 6
    tenMinInSeconds = 10*60
    
    for i in range(numOfTenMin):
        print("Waiting " + str(numOfTenMin - i) + "0 minutes to run again.")
        time.sleep(tenMinInSeconds)