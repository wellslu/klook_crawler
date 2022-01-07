import time
import datetime
import random
import pandas as pd
import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from activity_data import Get_Data
from database import Mongo_Database

default_args = {
'owner': 'wells',
'start_date': datetime.datetime(2021, 12, 31, 0, 0),
'depends_on_past': False,
'email': ['wellspitney@gmail.com'],
'email_on_failure': True,
'email_on_retry': True,
'schedule_interval':'0 0 * * *',
'retries': 1,
'retry_delay': datetime.timedelta(minutes=10),
}

def crawler():
    gt = Get_Data()
    today = str(datetime.date.today())
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
    mongo = Mongo_Database()
    mongo.connect_db("mongodb://mongo:27017/", 'klook_commodity', "Camping&Glamping")
    mongo.insert_data({'date':today,
                       'value': all_activities})
    mongo.client.close()
    
def make_daily_csv():
    today = str(datetime.date.today())
    mongo = Mongo_Database()
    mongo.connect_db("mongodb://mongo:27017/", 'klook_commodity', "Camping&Glamping")
    query = mongo.get_data({'date': today, 'value.reviews.rating': {'$lte': 80}})
    if query is None:
        print('error')
    data = pd.DataFrame.from_dict(list(query)[0]['value'])
    mongo.client.close()
    data['reviews'] = data['reviews'].apply(lambda x: list(filter(lambda y: y['rating'] <= 80, x)))
    data.to_csv('/usr/local/airflow/dags/Klook_Camping&Glamping_ratingUnder4.csv', index=False, encoding='utf-8-sig')
    
with DAG('klook', default_args=default_args) as dag:
    t1 = PythonOperator(task_id='crawler', python_callable=crawler, dag=dag)
    t2 = PythonOperator(task_id='make_csv', python_callable=make_daily_csv, dag=dag)
    t1 >> t2