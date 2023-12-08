import os
import json
from tqdm import tqdm
from collections import defaultdict


if __name__ == '__main__':
    data_dir = 'C:\\Users\\gary\\Desktop\\reportjson-all-in-all'
    record = defaultdict(list)
    for file in tqdm(os.listdir(f'{data_dir}')):
        try:
            with open(f'{data_dir}\\{file}', 'r', encoding='utf-8') as f:
                dct = json.loads(f.read())
            if 'strings' in dct['target']['file']:
                for s in dct['target']['file']['strings']:
                    if s.lower().find('bitcoin') != -1:
                        record[file].append(s)
            if 'procdump' in dct:
                for pd in dct['procdump']:
                    if 'strings' in pd:
                        for s in pd['strings']:
                            if s.lower().find('bitcoin') != -1:
                                record[file].append(s)
            if 'dropped' in dct:
                for drop_file in dct['dropped']:
                    if 'strings' in drop_file:
                        for s in drop_file['strings']:
                            if s.lower().find('bitcoin') != -1:
                                record[file].append(s)
            for pl in dct['CAPE']['payloads']:
                if 'strings' in pl:
                    for s in pl['strings']:
                        if s.lower().find('bitcoin') != -1:
                            record[file].append(s)
            if len(record[file]) != 0:
                with open(f"./statistical_result/bitcoin_keyword/{file.split('.')[0]}.txt", 'w') as f:
                    f.write('\n'.join(record[file]))
        except Exception as e:
            print(f'{file} error: {e}')
