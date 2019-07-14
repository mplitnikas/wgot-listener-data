import os
from botocore.vendored import requests
import boto3

database_resource = os.environ.get('StatsTable')
db_client = boto3.client('dynamodb')
url = os.environ.get('ListenersUrl')
callsign = os.environ.get('StationCallsign')

def lambda_handler(event, context):
    current_listeners = fetch_listeners(url)
    add_db_entry(database, current_listeners)

def fetch_listeners(url):
    resp = requests.get(url)
    #error handling if 400
    data = resp.json()

    feeds = data['icestats']['source']

    total_listeners = 0
    for feed in feeds:
        if feed.get('server_name') and callsign in feed.get('server_name'):
            total_listeners += ( feed.get('listeners') or 0 )

    return total_listeners

def add_db_entry(record):
    # expect object {'timestamp': int, 'listeners': int}
    timestamp = record.get('timestamp')
    listeners = record.get('listeners')
    if not timestamp or not listeners:
        return
    # insert item into db
