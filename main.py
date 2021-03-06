import datetime
import sys
import time
import selenium
from selenium import webdriver
import urllib.parse as urlparse
from urllib.parse import urlencode
import boto3
from botocore.exceptions import ClientError
from audioplayer import AudioPlayer

# Stevens pass ticket filters
NUMBER_OF_DAYS = 1
AGE_GROUP = 'Adult'
URL = 'https://www.stevenspass.com/plan-your-trip/lift-access/tickets.aspx'
WEB_DRIVER = './chromedriver'
TICKET_ELEMENT = 'liftTicketsResults__ticket'
MAX_NOTIFICATION = 5

# This address must be verified with Amazon SES.
SENDER = 'raychen0411@gmail.com'
ACCESS_KEY = ''
SECRET_KEY = ''
AWS_REGION = 'us-east-1'
SUBJECT = 'SP lift ticket is available on '

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ('Link: https://www.stevenspass.com/plan-your-trip/lift-access/tickets.aspx')

# The HTML body of the email.
BODY_HTML = '''<html>
    <head></head>
    <body>
      <h1>Link: https://www.stevenspass.com/plan-your-trip/lift-access/tickets.aspx</h1>
    </body>
    </html>
            '''
CHARSET = 'UTF-8'

# signal for play sound
play_sound = False


def find_tickets(date, address_list):
    print(str(datetime.datetime.now()) + ' Start find ticket: ' + date)
    # parse url
    params = {
        'startDate': date,
        'numberOfDays': NUMBER_OF_DAYS,
        'ageGroup': AGE_GROUP
    }
    url = parse_url(params, URL)
    print(url)

    dr = webdriver.Chrome(WEB_DRIVER)
    cnt = 0
    while True:
        dr.implicitly_wait(10)
        dr.get(url)
        try:
            my_dynamic_element = dr.find_element_by_class_name(TICKET_ELEMENT)
            print('Tickets found!!')
            print(my_dynamic_element.text)

            if play_sound:
                # play sound
                print('Play sound...')
                AudioPlayer("sound.mp3").play(block=True)
            else:
                # send email
                send_email(date, address_list)
                cnt += 1
                if cnt > MAX_NOTIFICATION:
                    break

        except selenium.common.exceptions.NoSuchElementException:
            print('No tickets found')

        print(str(datetime.datetime.now()) + ' wait 30 sec...')
        time.sleep(30)


def parse_url(params, url):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


def send_email(date, address_list):
    client = boto3.client('ses',
                          region_name='us-east-1',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': address_list
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT + date,
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print('Email sent! Message ID:'),
        print(response['MessageId'])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('[ERROR] Need at least 1 arguments, \'python main.py date\'')

    if len(sys.argv) < 3:
        play_sound = True

    if not play_sound and (not ACCESS_KEY or not SECRET_KEY):
        raise Exception('[ERROR] AWS account access key or secret key is '
                        'missing')

    recipient_list = []
    for i in range(2, len(sys.argv)):
        recipient_list.append(sys.argv[i])
    find_tickets(sys.argv[1], recipient_list)
