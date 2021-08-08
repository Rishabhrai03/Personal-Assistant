import json
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# set your social credentials in Credentials.txt file
account = open('../Credentials.txt', 'r').read()
Account = json.loads(account)
print("Credentials Here:-", Account['Twitter']['UserId'])
print("Credentials Here:-", Account['Twitter']['password'])

driver = webdriver.Chrome()

def get_twitter_account():
    driver.get("https://twitter.com/login")

    userid_Xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input'
    pass_Xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input'
    login_btn_Xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div'
    time.sleep(3)

    driver.find_element_by_id(userid_Xpath).send_keys(Account['Twitter']['UserId'])
    time.sleep(0.5)
    driver.find_element_by_id(pass_Xpath).send_keys(Account['Twitter']['password'])
    time.sleep(0.5)
    driver.find_element_by_id(login_btn_Xpath).click()
