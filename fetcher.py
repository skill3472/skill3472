import requests
from datetime import datetime, timedelta
import sys
import yaml

with open('config.yaml', 'r') as c:
    config = yaml.safe_load(c)
key = sys.argv[1]
api = 'https://api.monkeytype.com'

time = config['time']

def get_pb():
    endpoint = f'{api}/users/personalBests'
    query = {
    "mode": "words",
    "mode2":"50"
    }
    apekey = f'ApeKey {key}'
    print('Requesting with ApeKey ' + apekey)
    x = requests.get(endpoint, headers={'Authorization':apekey, 'Accept':'application/json'}, \
                     allow_redirects=True, params=query)
    response = x.json()
    pb = [response['data'][0]['wpm'], response['data'][0]['acc']]
    return pb

def changeLine(n, text):
    with open(config['out_file'], 'r', encoding='utf-8') as f:
        data = f.readlines()
    data[n] = text
    with open(config['out_file'], 'w', encoding='utf-8') as f:
        f.writelines(data)

def updateFile():
    pb = get_pb()
    now = (datetime.now() + timedelta(hours=2)).strftime(time)
    text = f'My current MonkeyType PB is - WPM:{pb[0]} Acc:{pb[1]}\n'
    timestamp = f'Updated on: {now}\n'
    console_timestamp = '[%H:%M:%S]'
    print(f'{datetime.now().strftime(console_timestamp)} Updated the file!')
    changeLine(config['out_line'], text)
    if (config['timestamp_line'] >= 0):
        changeLine(config['timestamp_line'], timestamp)

if __name__ == '__main__':
    print('-'*40 + '\nWelcome to PBFetcher by skill3472!\n' + '-'*40)
    updateFile()
