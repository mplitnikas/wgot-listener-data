import os
from botocore.vendored import requests
import boto3
import time

database_resource = os.environ.get('StatsTable')
db_client = boto3.client('dynamodb')
url = os.environ.get('ListenersUrl')
callsign = os.environ.get('StationCallsign')

def lambda_handler(event, context):
    current_listeners = str(fetch_listeners(url))
    timestamp = str(int(time.time()))
    add_db_entry(timestamp, current_listeners)

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

def add_db_entry(timestamp, listeners):
    if not timestamp or not listeners:
        return
    db_client.put_item(
        TableName=database_resource,
        Item={
            'timestamp': { 'N': timestamp },
            'listeners': { 'N': listeners }
    })
