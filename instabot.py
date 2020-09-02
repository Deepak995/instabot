import requests
import selenium
import time
import pdb
from selenium import webdriver
import logging
import re
import datetime
import os
import openpyxl
from selenium.webdriver.support.select import Select
class instabot:
    def __init__(self, username, pas):
        self.user = username
        self.password = pas
        self.driver = webdriver.Chrome('/webdriver/chromedriver')
        self.date_obj = datetime.date.today()

    def opening_files_for_data_saving(self, name):
        parent_dir = 'D:/'
        directory = name
        dirr = os.path.join(parent_dir, directory+'/')
        if os.path.exists(dirr):
            print('path exist')
        else:
            print("making a new directory: "+ dirr)
            os.mkdir(dirr)
        if os.path.exists(dirr+ name + '.xlsx'):
            print('opening the xlsx file: '+ dirr + '/' + name +'.xlsx')
            wb = openpyxl.load_workbook(dirr + '/' + name + '.xlsx')
            sheet = wb[name]
        else:
            path = os.getcwd()
            print(path)
            print('creating a new xlsx file for the data base: '+ dirr + '/' + name +'.xlsx')
            wb = openpyxl.Workbook()
            sheet = wb.create_sheet(index=0, title=name)
        return dirr, wb, sheet

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
        self.opening_files_for_data_saving(username)

    def fetching_followings_count_info(self):
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
            """, scrollbox)
            time.sleep(3)
        links = scrollbox.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        names = set(names)
        print("***********you are following these many people = {}***************".format(len(names)))
        count = len(names)
        self.driver.find_element_by_xpath('//div[@class="WaOAr"]//button[@class="wpO6b "]//div').click()
        print("saving the following list in an excel file")
        # opening the xlsx(excel) file where the following names is needed to be saved
        directoy, wb_obj, sheet = self.opening_files_for_data_saving(self.user)
        lenn = len(sheet['A'])
        sheet['A' + str(lenn + 1)] = '***NAME OF THE USERS YOU ARE FOLLOWING on date' + str(self.date_obj) + '***'
        sheet.column_dimensions['A'].width = 70
        for name, i in zip(names, range(lenn+2, lenn+count+1)):
            sheet['A'+str(i)] = name
        wb_obj.save(directoy+self.user+'.xlsx')
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
        print("saving the followers list in an excel file")
        # opening the xlsx(excel) file where the followers names is needed to be saved
        directoy, wb_obj, sheet = self.opening_files_for_data_saving(self.user)
        pdb.set_trace()
        lenn = len(sheet['B'])
        sheet['B' + str(lenn + 1)] = '***NAME OF UR FOLLOWERS on date' + str(self.date_obj) + '***'
        sheet.column_dimensions['B'].width = 70
        for name, i in zip(names, range(lenn+2, lenn+count+1)):
            sheet['B'+str(i)] = name
        wb_obj.save(directoy+self.user+'.xlsx')
        return count, names

    def fetching_greedy_people(self, following_names, followers_names):
        cheap_ppl = []
        for name in following_names:
            if name not in followers_names:
                cheap_ppl.append(name)
        cheap_ppl_count = len(cheap_ppl)
        print('**********************People count who does not deserve to follow - {}***********************'.format(cheap_ppl_count))
        print('*****************THE PEOPLE WHOME YOU NEED TO TAKE ACTION FOR **************')
        print("saving the greedy people list  in an excel file")
        directoy, wb_obj, sheet = self.opening_files_for_data_saving(self.user)
        lenn = len(sheet['C'])
        sheet['C' + str(lenn + 1)] = '**THE PEOPLE WHOME YOU NEED TO TAKE ACTION FOR' + str(self.date_obj) + '**'
        for name, i in zip(cheap_ppl, range(lenn+2, lenn+cheap_ppl_count+1)):
            sheet['C'+str(i)] = name
        wb_obj.save(directoy + self.user + '.xlsx')
        return cheap_ppl_count, cheap_ppl

    def action_on_greedy_people(self, cheap_ppl):
        directoy, wb_obj, sheet = self.opening_files_for_data_saving(self.user)
        #self.login('deepak_choudhary_777', 'instagram295')
        unfollowing_ppl = []
        directoy, wb_obj, sheet = self.opening_files_for_data_saving(self.user)
        lenn_unfolled = len(sheet['D'])
        sheet['D'+str(lenn_unfolled+1)] = '**Peaple you have unfollowed on date'+str(self.date_obj)+'**'
        lenn_unfolled += 1
        lenn_not_unfollowed = len(sheet['E'])
        sheet['E' + str(lenn_not_unfollowed + 1)] = '**Peaple you did not unfollowed on date'+str(self.date_obj)+'**'
        lenn_not_unfollowed += 1
        for k in cheap_ppl:
            time.sleep(2)
            self.driver.get('https://www.instagram.com/{}/'.format(k))
            try:
                self.driver.find_element_by_xpath('//div[contains(@class,"error-container" )]')
                logging.warning('Loading error for user {} '.format(k))
                continue
            except:
                logging.info('loaded successfully moving forward')

            time.sleep(3)
            total_post = self.driver.find_element_by_xpath('//span[@class="-nal3 "]//span[@class="g47SY "]').text
            if re.search(r',', total_post):
                total_post = total_post.replace(',', '')
            if int(total_post) < 600:
                logging.info('!!!!!!!!!!!!!!!!unfollowing : {}'.format(k))
                #self.driver.find_element_by_xpath('//span[@class="vBF20 _1OSdk"]//button').click()
                #self.driver.find_element_by_xpath('//button[contains(text(), "Unfollow")]').click()
                unfollowing_ppl.append(k)
                print("saving unfollowed people name in excel ")
                sheet['D' + str(lenn_unfolled+1)] = k + '- no of post :'+total_post
            else:
                print("saving people name whome  you did not unfollowed in excel ")
                sheet['E' + str(lenn_not_unfollowed+1)] = k + '- no of post :'+total_post

        wb_obj.save(directoy+self.user+'.xlsx')
obj = instabot('deepak_choudhary_777', 'instagram295')
obj.login('deepak_choudhary_777', 'instagram295')
following_count, following_names = obj.fetching_followings_count_info()
followers_count, followers_names = obj.fetching_followers_count_info()
cheap_ppl_count, cheap_ppl = obj.fetching_greedy_people(following_names, followers_names)
obj.action_on_greedy_people(cheap_ppl)