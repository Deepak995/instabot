import instabot
import time
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as b
from selenium import webdriver
driver = webdriver.Chrome('/webdriver/chromedriver')
ins = instabot.instabot(driver,'', '')
ins.login()
max_likes = 100
max_follows = 100
def get_follwers():
    count, names = ins.returns_followers_names('seju_craft_industry_16')
    L = 0
    F = 0
    for name in names:

        driver.get('https://www.instagram.com/{}/'.format(name))
        try:
            driver.find_element_by_xpath('//div[contains(@class,"error-container" )]')
            logging.warning('Loading error for user {} '.format(name))
            ins.login()
            continue
        except:
            logging.info('loaded successfully moving forward')
        time.sleep(2)
        if ins.is_public():
            print(name+' public account')
            print('current likes: ' + str(L))
            if L < max_likes:
                try:
                    ins.follow_page()
                    print('page '+name+' followed successfully')
                    F += 1
                    try:
                        ins.like_post()
                        L += 1
                        print("POST LIKED for " + name)
                        print('current follows: ' + str(F))
                    except:
                        print('could not like..lets follow instead')
                except:
                    print('could not follow the page '+ name)
        else:
            print(name+' account is private')
            print('current follows: ' + str(F))
            if F < max_follows:
                time.sleep(2)
                try:
                    ins.follow_page()
                    print('page '+name+' followed successfully')
                    F += 1
                except:
                    print('could not follow the page '+ name)
def smart_unfollw():
    following_count, following_names = ins.fetching_followings_count_info()
    followers_count, followers_names = ins.fetching_followers_count_info()
    cheap_ppl_count, cheap_ppl = ins.fetching_greedy_people(following_names, followers_names)
    ins.action_on_greedy_people(cheap_ppl)
if __name__ == '__main__':
	#get_follwers()
    smart_unfollw()