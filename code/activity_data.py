import requests
import time
import math
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

class Get_Data(object):
    def __init__(self):
        self.driver = None
        self.open_driver()
    
    @staticmethod
    def get_activities(start):
        headers = {'accept-language': 'zh_TW', 'currency': 'TWD'}
        res = requests.get(f'https://www.klook.com/v1/experiencesrv/category/activity?frontend_id_list=19&size=24&start={start}', headers=headers)
        activities = res.json()['result']['activities']
        time.sleep(random.randint(1, 5))
        return activities
        
    def open_driver(self):
        if self.driver is not None:
            self.driver.quit()
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36')
        self.driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',
                                       desired_capabilities=DesiredCapabilities.CHROME,
                                      options=chrome_options)
#         self.driver = webdriver.Chrome(chrome_options=chrome_options)
    
    def get_review(self, activity):
        if '評價' in activity['review_hint']:
            review_num = min(170, int(activity['review_hint'].split(' ')[0]))
        else:
            return []
        activity_id = activity['activity_id']
        reviews = []
        for page in range(1, math.ceil(review_num/10)+1):
            self.driver.get(f'https://www.klook.com/v1/usrcsrv/activities/{activity_id}/reviews?page={page}&limit=10')
            if 'Please verify you are a human' in self.driver.page_source:
                self.open_driver()
                self.driver.get(f'https://www.klook.com/v1/usrcsrv/activities/{activity_id}/reviews?page={page}&limit=10')
                print('verify appear: restart driver')
            while 'Please verify you are a human' in self.driver.page_source:
                print('verify still exist: do verify')
                time.sleep(3)
                ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_xpath("/html/body/section/div[2]/div/h1"), 80, 80).click_and_hold().perform()
                time.sleep(random.randint(8, 15))
                ActionChains(self.driver).move_by_offset(random.randint(50, 100),random.randint(50, 100)).click().perform()
                ActionChains(self.driver).move_by_offset(random.randint(50, 100),random.randint(50, 100)).click().perform()
                time.sleep(random.randint(10, 30))
            reviews+=json.loads(self.driver.page_source.split('pre-wrap;">')[1].split('\n</pre>')[0])['result']['item'].copy()
            time.sleep(random.randint(1, 3))
            if page % 10 == 0:
                time.sleep(random.randint(3, 5))
        return reviews