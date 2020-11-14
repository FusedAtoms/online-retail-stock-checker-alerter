#!/usr/bin/env python3
""" Online Retail Stock Checker and Alerter """
import sys
import time
import logging
from signal import signal, SIGINT
from selenium import webdriver
from selenium import common
from twilio.rest import Client

psdirect = {
    'url': 'https://direct.playstation.com/en-us/consoles/console/',
    'products': [
        {
            #'id': 'playstation-4-pro-1tb-console.3003346', #PS4 link for testing
            'id': 'playstation5-digital-edition-console.3005817',
            'name': "PS5 Digital",
            'last_alert': -1,
        },
        {
            'id': 'playstation5-console.3005816',
            'name': "PS5 Disc",
            'last_alert': -1,
        },
    ]
}

amazon = {
    'url': 'https://www.amazon.com/gp/product/',
    'products': [
        {
            #'id': 'B077QT6K94', #PS4 link for testing
            'id': 'B08FC6MR62',
            'name': "PS5 Digital",
            'retail': 400,
            'last_alert': -1,
        },
        {
            'id': 'B08FC5L3RG',
            'name': "PS5 Disc",
            'retail': 500,
            'last_alert': -1,
        },
    ]
}

def print_oos(site, name):
    """ Print out of stock message """

    logger.info(site + '\t: ' + name + '\t: OUT OF STOCK')


def print_is(site, name):
    """ Print in stock message """

    logger.info(site + '\t: ' + name + '\t: IN STOCK')


def send_sms(site, product, url):
    """ Send in stock text message """

    elapsed = time.perf_counter() - product['last_alert']
    #Only send once every 5 minutes if there's stock
    if product['last_alert'] < 0 or elapsed > 300:
        logger.debug("Sending text message")
        account_sid = user_data['TWILIO_ACCOUNT_SID']
        auth_token = user_data['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        client.messages.create(
                            body=product['name'] + ' is Available from ' \
                                + site + '\n' + url+product['id'],
                            from_=user_data['TWILIO_SENDER_NUM'],
                            to=user_data['TWILIO_RECEIVER_NUM']
                        )
        product['last_alert'] = time.perf_counter()


def check_playstation_direct(browser):
    """ Check PSDirect website stock """

    for product in psdirect['products']:
        logger.debug("Opening URL: " + psdirect['url'] + product['id'])
        browser.get(psdirect['url'] + product['id'])

        box = browser.find_elements_by_class_name('button-placeholder')
        for elem in box:
            button = elem.find_elements_by_class_name("add-to-cart")
            if len(button) > 0 and "hide" in button[0].get_attribute('class'):
                print_oos('PSDirect', product['name'])
            else:
                print_is('PSDirect', product['name'])
                send_sms("PS Direct", product, psdirect['url'])
            break


def check_amazon(browser):
    """ Check Amazon website stock """

    for product in amazon['products']:
        logger.debug("Opening URL: " + amazon['url'] + product['id'])
        browser.get(amazon['url'] + product['id'])

        #Check if currently unavailable
        try:
            box = browser.find_element_by_id('availability')
        except common.exceptions.NoSuchElementException as e:
            #Likely an error with the get response
            logger.error("Error finding element", exc_info = e)
            print_oos("Amazon", product['name'])
            continue

        elems = box.find_elements_by_class_name('a-color-price')
        is_oos = False
        for elem in elems:
            if "currently unavailable" in elem.text.lower():
                is_oos = True
                print_oos("Amazon", product['name'])
                break
        if is_oos:
            continue

        #Check if available from other sellers
        elems = box.find_elements_by_link_text("these sellers")
        if len(elems) > 0:
            print_oos("Amazon", product['name'])
            continue

        #Check if over retail price
        elem = browser.find_element_by_id('priceblock_ourprice')
        if float(elem.text[1:]) > product['retail']:
            print_oos("Amazon", product['name'])
            continue

        print_is("Amazon", product['name'])
        send_sms("Amazon", product, amazon['url'])


def setup_exit_signal(browser):
    """ Script setup """

    def exit_handler(*args):
        """ Ctrl-C signal handler """

        print("Exiting script...")
        logger.debug("Closing Chrome Browser")
        browser.quit()
        sys.exit(0)

    signal(SIGINT, exit_handler)

    
def setup_logger():
    """ Configure logger """
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def get_user_data():
    """ Gather user Twilio data """
    data = {
        'TWILIO_ACCOUNT_SID': '',
        'TWILIO_AUTH_TOKEN': '',
        'TWILIO_SENDER_NUM': '',
        'TWILIO_RECEIVER_NUM': ''
    }
    print("Enter Twilio Account SID: ")
    data['TWILIO_ACCOUNT_SID'] = input()
    print("Enter Twilio Authentication Token: ")
    data['TWILIO_AUTH_TOKEN'] = input()
    print('Enter Twilio Phone Number: ')
    data['TWILIO_SENDER_NUM'] = input()
    print('Enter Your Phone Number (with country code): ')
    data['TWILIO_RECEIVER_NUM'] = input()

    return data


def main():
    """ Script entry point """
    setup_logger()
    logger.debug('Opening Chrome Browser')
    browser = webdriver.Chrome()
    setup_exit_signal(browser)

    while True:
        check_amazon(browser)
        check_playstation_direct(browser)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    user_data = get_user_data()
    main()
