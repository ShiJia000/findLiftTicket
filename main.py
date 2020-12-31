import sys
import time
import selenium
from selenium import webdriver
import urllib.parse as urlparse
from urllib.parse import urlencode

NUMBER_OF_DAYS = 1
AGE_GROUP = "Adult"
URL = "https://www.stevenspass.com/plan-your-trip/lift-access/tickets.aspx"
WEB_DRIVER = "./chromedriver"
TICKET_ELEMENT = "liftTicketsResults__ticket"


def find_tickets(date):
    print("Start find ticket: " + date)
    # parse url
    params = {
        'startDate': date,
        'numberOfDays': NUMBER_OF_DAYS,
        'ageGroup': AGE_GROUP
    }
    url = parse_url(params, URL)
    print(url)

    dr = webdriver.Chrome(WEB_DRIVER)
    while True:
        dr.implicitly_wait(10)
        dr.get(url)
        try:
            myDynamicElement = dr.find_element_by_class_name(TICKET_ELEMENT)
            print("Tickets found!!")
            print(myDynamicElement.text)
            break
        except selenium.common.exceptions.NoSuchElementException:
            print("No tickets found")

        print("Wait 1min...")
        time.sleep(5)


def parse_url(params, url):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


if __name__ == '__main__':
    find_tickets(sys.argv[1])
