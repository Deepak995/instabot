import requests
import selenium
import time
import pdb
from selenium import webdriver
import logging
import re
import datetime
import os
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select
class instabot:
    driver = webdriver.Chrome('/webdriver/chromedriver')
    date_obj = datetime.date.today()
    def login(self, username, password ):
        try:
            self.driver.get('https://www.instagram.com/')
        except:
            logging.error('failed to load please check internet connection or the url, if it is correct?')
        time.sleep(2)
        self.driver.find_element_by_xpath('//input[contains(@aria-label,"username")]').send_keys(username)
        self.driver.find_element_by_xpath('//input[contains(@aria-label,"Password")]').send_keys(password)
        self.driver.find_element_by_xpath('//div[contains(text(), "Log In" )]').click()
        time.sleep(4)
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now" )]').click()
        time.sleep(4)
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        parent_dir = 'D:/'
        directory = 'insta'
        dirr = os.path.join(parent_dir, directory)
        os.mkdir(dirr)

    def fetching_followings_count_info(self):
        #self.login('deepak_choudhary_777', 'instagram295')
        time.sleep(3)
        self.driver.find_element_by_xpath('//div[@class="RR-M-  _2NjG_"]//a[@class="_2dbep qNELH kIKUG"]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//a[contains(@href, "following")]').click()
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
        #last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        last_ht, ht =0, 1
        time.sleep(3)
        scrollbox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')

        while last_ht != ht:
            last_ht = ht
            # Scroll down to bottom
            #self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            #self.driver.execute_scrript("arguments[0].scrollIntoView();",element)
            # Wait to load page
            ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;                        
            """, scrollbox )
            time.sleep(3)
        links = scrollbox.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        names = set(names)
        print("***********you are following these many people = {}***************".format(len(names)))
        count = len(names)
        self.driver.find_element_by_xpath('//div[@class="WaOAr"]//button[@class="wpO6b "]//div').click()
        f = open('D:/insta/following'+str(self.date_obj)+'.txt', 'w')
        f.write('*****************NAME OF THE USERS YOU ARE FOLLOEING **************')
        for ele in names:
            f.write('\n'+ ele + '\n')
        f.close()
        return count, names

    def fetching_followers_count_info(self):
        #self.login('deepak_choudhary_777', 'instagram295')
        time.sleep(3)
        #self.driver.find_element_by_xpath('//div[@class="RR-M-  _2NjG_"]//a[@class="_2dbep qNELH kIKUG"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//a[contains(@href, "followers")]').click()
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
        last_ht, ht =0, 1
        time.sleep(1)
        scrollbox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        while last_ht != ht:
            last_ht = ht
            # Scroll down to bottom
            ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;                        
            """, scrollbox )
            # Wait to load page
            time.sleep(2)
        links = scrollbox.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        names = set(names)
        count = len(names)
        print("***********YOUR FOLLOWERS COUNT = {}***************".format(len(names)))
        self.driver.find_element_by_xpath('//div[@class="WaOAr"]//button[@class="wpO6b "]//div').click()
        f = open('D:/insta/followers'+str(self.date_obj)+'.txt', 'w')
        f.write('*****************NAME OF UR FOLLOWERS **************')
        for ele in names:
            f.write('\n'+ ele + '\n')
        f.close()
        return count, names

    def fetching_greedy_people(self, following_names, followers_names):
        cheap_ppl = []
        for name in following_names:
            if name not in followers_names:
                cheap_ppl.append(name)
        cheap_ppl_count = len(cheap_ppl)
        print('**********************People count who does not deserve to follow - {}***********************'.format(cheap_ppl_count))
        f = open('D:/insta/greedy'+str(self.date_obj)+'.txt', 'w')
        f.write('*****************THE PEOPLE WHOME YOU NEED TO TAKE ACTION FOR **************')
        for ele in cheap_ppl:
            f.write(ele + '\n')
        f.close()
        return cheap_ppl_count, cheap_ppl

    def action_on_greedy_people(self, cheap_ppl):
        #self.login('deepak_choudhary_777', 'instagram295')
        unfollowing_ppl = []
        #f = open('D:/insta/unfollowed' + str(self.date_obj) + '.txt', 'w')
        #f.write('*****************PEOPLE YOU HAVE UNFOLLOWED : {} **************')
        #for k in cheap_ppl:
        time.sleep(2)
        req = requests.get('https://www.instagram.com/{}/'.format(cheap_ppl))
        soup = BeautifulSoup(req.text,'html.parser')
        result = soup.find('span', attrs={'class' : "g47SY "}).get_text
        pdb.set_trace()
        #
        #     try:
        #         self.driver.find_element_by_xpath('//div[contains(@class,"error-container" )]')
        #         logging.warning('Loading error for user {} '.format(k))
        #         continue
        #     except:
        #         logging.info('loaded successfully moving forward')
        #
        #     time.sleep(3)
        #     total_post = self.driver.find_element_by_xpath('//span[@class="-nal3 "]//span[@class="g47SY "]').text
        #     if re.search(r',', total_post):
        #         total_post = total_post.replace(',', '')
        #     if int(total_post) < 600:
        #         logging.info('!!!!!!!!!!!!!!!!unfollowing : {}'.format(k))
        #         #self.driver.find_element_by_xpath('//span[@class="vBF20 _1OSdk"]//button').click()
        #         #self.driver.find_element_by_xpath('//button[contains(text(), "Unfollow")]').click()
        #         unfollowing_ppl.append(k)
        #         f.write(k+': ' +total_post+ '\n')
        #     else:
        #         j = open('D:/insta/did_not_unfollowed' + str(self.date_obj) + '.txt', 'w')
        #         j.write(k + '- no of post :'+total_post+'\n')
        #
        # f.close()
        # j.close()
obj = instabot()
obj.login('deepak_choudhary_777', 'instagram295')
#following_count, following_names = obj.fetching_followings_count_info()
#followers_count, followers_names = obj.fetching_followers_count_info()
#cheap_ppl_count, cheap_ppl = obj.fetching_greedy_people(following_names, followers_names)
obj.action_on_greedy_people('sejal_pawar16')