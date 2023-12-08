from config import ransomware_csv_dir, benign_csv_dir, result_dir
from utils import is_clean_domain
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import os
import json
from tqdm import tqdm


if __name__ == '__main__':
    http_get_file_count = defaultdict(int)
    http_get_file_list = defaultdict(list)
    for file in tqdm(os.listdir(ransomware_csv_dir)):
        sample_id = int(file.split('.')[0])
        try:
            df = pd.read_csv(f'{ransomware_csv_dir}/{file}', index_col=0)
            existed = set()
            for idx, row in df.iterrows():
                if row['protocol'] == 'HTTP':
                    if row['info'].startswith('GET'):
                        file_name = row['info'].split(' ')[1]
                        if file_name not in existed:
                            http_get_file_count[file_name] += 1
                            existed.add(file_name)
                        http_get_file_list[sample_id].append(file_name)
        except:
            print(f"{sample_id} error!")

    with open(f'{result_dir}/http_get_file_count.json', 'w') as f:
        f.write(json.dumps(http_get_file_count))

    for sample_id in http_get_file_list:
        with open(f"{result_dir}/http_get_file/{sample_id}.csv", 'w', encoding='utf-8') as f:
            for get_file in http_get_file_list[sample_id]:
                f.write(f'{get_file},{http_get_file_count[get_file]}\n')
