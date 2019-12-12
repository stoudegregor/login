import sys
import time
import json
import logging
from selenium import webdriver
import getpass
import smtplib as SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)], level=logging.INFO)
log = logging.getLogger(__name__)


def smsmessage():
    #you need to turn on the "Less secure app access" feature for your google account
    email = 'email'
    password = getpass.getpass()

    send_to = 'phone_number'
    smtp_client = 'smtp.gmail.com'
    port_number = 465

    server = SMTP.SMTP_SSL(smtp_client, port_number)
    server.login(email, password)

    message = MIMEMultipart()
    message["Subject"] = 'Subject: Testing SMTP and MIME text message'
    body = 'Body: Testing SMTP and MIME text message'

    message.attach(MIMEText(body, 'plain'))
    sms = message.as_string()

    server.sendmail(email, send_to, sms)
    server.quit()

def login(site):
    log.info('Opening config file')
    with open('config.json') as f:
        data = json.load(f)
        seleniumlocation = data['selenium']
        jdatasite = data['sites'][site]

        if site in data['sites']:
            log.info('Found {} data'.format(site))
            url = jdatasite['url']
            uname = jdatasite['usernameinput']
            ubutton = jdatasite['usernamebutton']
            pwname = jdatasite['passwordinput']
            pwbutton = jdatasite['passwordbutton']


            chromeopts=webdriver.ChromeOptions()
            log.debug(chromeopts.add_argument('--incognito'))
            u = jdatasite['users']

            for user in jdatasite['users']:
                driver = webdriver.Chrome(seleniumlocation, chrome_options=chromeopts)
                log.debug(driver.get(url))
                log.info('Logging in {}'.format(user))

                username = driver.find_element_by_id(uname)
                usernext = driver.find_element_by_id(ubutton)
                log.debug(username.send_keys(u[user]['email']))
                log.debug(usernext.click())

                password = u[user]['password']
                passwordxpath = pwname
                time.sleep(10)
                passwordinput = driver.find_element_by_xpath(passwordxpath)
                passwordinput.send_keys(password)
                passwordnext = driver.find_element_by_id(pwbutton)
                log.debug(passwordnext.click())
                time.sleep(10)

                driver.close()
                
