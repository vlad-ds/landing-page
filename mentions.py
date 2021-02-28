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
    print('WARNING: Could not retrieve API KEY.')

def get_mentions(keyword, delta=15):
    '''Access news API to get a topic's mentions and headlines
    in the past <delta> days.'''

    today = datetime.today().date()
    today_str = f"{today.year}-{today.month}-{today.day}"
    filecache = f"{keyword}_{today_str}.json"
    cache_folder = '.newscache'

    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)


    if filecache in os.listdir(cache_folder):
        print('Loading from cache')
        with open(os.path.join(cache_folder, filecache)) as file:
            result = json.load(file)
            return result
    else:
        #clearing old files (on the same keyword) from cache
        for file in os.listdir(cache_folder):
            if file.startswith(keyword):
                path = os.path.join(cache_folder, file)
                os.remove(path)

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
            print('Request failed')
            failed_requests += 1
            result['mentions'].append((x_date, None))

        sel += day


    if failed_requests <= delta // 3:
        print('Caching results...')
        with open(os.path.join(cache_folder, filecache), 'w') as file:
            json.dump(result, file)
    else:
        print('Too many null results. Not caching.')

    return result

def plot_mentions(mentions_dict):
    date, count = zip(*mentions)
    fig = go.Figure(data=go.Scatter(x=date, y=count))
    fig.update_layout(title='News Headlines Mentioning Dogs (Past 15 days)',
                   xaxis_title='Day',
                   yaxis_title='Doglines')
    return fig
