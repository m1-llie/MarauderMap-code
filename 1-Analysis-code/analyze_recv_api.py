import os
from tqdm import tqdm
import json
from collections import defaultdict


d = defaultdict(int)

api_file_cnt = defaultdict(int)
api_total_cnt = defaultdict(int)

for file in tqdm(os.listdir('./statistical_result/network_activity')):
    with open(f'./statistical_result/network_activity/{file}', 'r') as f:
        dct = json.loads(f.read())
    existed = set()
    for process in dct:
        for calls in dct[process][2]:
            if calls['api'].lower().find('recv') != -1:
                api = calls['api']
                if api not in existed:
                    api_file_cnt[api] += 1
                    existed.add(api)
                api_total_cnt[api] += 1

for api in api_file_cnt:
    print(api, api_total_cnt[api], api_file_cnt[api], api_total_cnt[api] / api_file_cnt[api])
