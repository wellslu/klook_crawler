import time
import random
import pandas as pd
from activity_data import Get_Data
from database import Mongo_Database

gt = Get_Data()
mongo = Mongo_Database()

if __name__ == '__main__':
    all_activities = []
    start = 1
    while True:
        activities = gt.get_activities(start)
        if not activities:
            break
        all_activities+=activities.copy()
        print(f'get page {start} activities')
        start+=1
    for index, activity in enumerate(all_activities):
        reviews = gt.get_review(activity)
        all_activities[index]['reviews'] = reviews
        activity_id = activity['activity_id']
        print(f'get {activity_id} reviews')
        if index % 15 == 0:
            time.sleep(random.randint(5, 10))
    gt.driver.quit()
    
    mongo.connect_db("mongodb://mongo:27017/", 'klook_commodity', "Camping&Glamping")
    mongo.insert_data(all_activities)
    query = mongo.get_data({'reviews.rating': {'$lte': 80}})
    if query is None:
        print('error')
    data = pd.DataFrame(list(query))
    mongo.client.close()
    data['reviews'] = data['reviews'].apply(lambda x: list(filter(lambda y: y['rating'] <= 80, x)))
    data.to_csv('./Klook_Camping&Glamping_ratingUnder4.csv', index=False, encoding='utf-8-sig')

