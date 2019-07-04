import os
import requests

database = os.environ.get('StatsTable')
url = os.environ.get('ListenersUrl')
callsign = os.environ.get('StationCallsign')
#url="http://pacificaservice.org:8000/status-json.xsl"

def lambda_handler(event, context):
    if not database:
        raise Exception('database env variable not set: StatsTable')
    if not url:
        raise Exception('url env variable not set: ListenersUrl')

    current_listeners = fetch_listeners(url)


def fetch_listeners(url):
    resp = requests.get(url)
    #error handling if 400
    #data = json.loads(resp.content.decode('utf-8'))
    data = resp.json()

    feeds = data['icestats']['source']

    total_listeners = 0
    for feed in feeds:
        if feed.get('server_name') and callsign in feed.get('server_name'):
            total_listeners += ( feed.get('listeners') or 0 )

    return total_listeners

def update_db(record):
    # expect object {'timestamp': int, 'listeners': int}
    
