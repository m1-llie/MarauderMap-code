import os
from tqdm import tqdm
import json
from collections import defaultdict


apis = {
    'send',
    'WSASend',
    'WinHttpOpenRequest',
    'WinHttpSendRequest',
    'HttpOpenRequestA',
    'HttpSendRequestA',
    'HttpOpenRequestW',
    'HttpSendRequestW',
    'sendto'
}

api_total_cnt = defaultdict(int)
api_file_cnt = defaultdict(int)

for file in tqdm(os.listdir('./statistical_result/network_activity')):
    with open(f'./statistical_result/network_activity/{file}', 'r') as f:
        dct = json.loads(f.read())

    exist_api = set()
    for process in dct:
        for calls in dct[process][2]:
            api = calls['api']
            if api in apis:
                api_total_cnt[api] += 1
            if api not in exist_api:
                api_file_cnt[api] += 1
                exist_api.add(api)

for api in api_total_cnt:
    print(api, api_total_cnt[api], api_file_cnt[api])
