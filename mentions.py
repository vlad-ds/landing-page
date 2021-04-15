import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os, shutil
import json

API_KEY = os.environ.get('API_KEY')

if API_KEY:
    print(f'API_KEY of length {len(API_KEY)} retrieved.')
else:
    print('Retrieving API KEY locally.')
    try:
        with open('.env') as file:
            API_KEY = file.read().split('=')[1].strip()
            print(f'API_KEY of length {len(API_KEY)} retrieved.')
    except:
        print("Error. Could not find local API KEY.")

def get_mentions(keyword, delta=15):
    '''Access news API to get a topic's mentions and headlines
    in the past <delta> days.'''

    today = datetime.today().date()
    today_str = f"{today.year}-{today.month}-{today.day}"
    filecache = f"{keyword}_{today_str}.json"
    cache_folder = '.newscache'

    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)

    #load from cache if available
    if filecache in os.listdir(cache_folder):
        print('Loading from cache')
        with open(os.path.join(cache_folder, filecache)) as file:
            result = json.load(file)
            return result

    #did not load from cache: try to retrieve fresh data
    month = timedelta(days=delta)
    day = timedelta(days=1)

    result = {
    'mentions': [],
    'headlines': []
    }

    sel = today - month
    failed_requests = 0

    while sel < today:

        start = sel
        end = sel + day
        x_date = f"{end.day}/{end.month}"

        endpoint = 'https://newsapi.org/v2/everything'
        params = {'apiKey': API_KEY,
                  'qInTitle': keyword,
                  'from': start.isoformat(),
                  'to': end.isoformat()}

        resp = requests.get(endpoint, params)

        if resp.ok:
            print('Request succeeded')
            count = resp.json().get('totalResults')
            result['mentions'].append((x_date, count))
            heads = [(art['title'], art['url']) for art in resp.json().get('articles')]
            result['headlines'] += heads
        else:
            print(f'Request failed. Status {resp.status_code}')
            print(resp.text)
            failed_requests += 1
            result['mentions'].append((x_date, None))

        sel += day


    if failed_requests <= delta // 3:
        print('Clearing cache...')
        #clearing old files (on the same keyword) from cache
        for file in os.listdir(cache_folder):
            path = os.path.join(cache_folder, file)
            if file.startswith(keyword):
                os.remove(path)
        #¢aching fresh results
        print('Caching results...')
        with open(os.path.join(cache_folder, filecache), 'w') as file:
            json.dump(result, file)
    else:
        #if we could not get fresh results, we load from cache
        print('Too many null results. Not caching.')
        print('Loading from cache...')
        last_file = [file for file in os.listdir(cache_folder)
                     if file.startswith(keyword)
                     ][0]
        with open(os.path.join(cache_folder, last_file)) as file:
            result = json.load(file)
            return result
    return result
