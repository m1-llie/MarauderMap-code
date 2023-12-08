import os
from tqdm import tqdm
import pandas as pd
from config import ransomware_csv_dir, result_dir
from collections import defaultdict
import json


if __name__ == '__main__':
    all_sample_ip_count = defaultdict(lambda: defaultdict(int))
    for file in tqdm(os.listdir(ransomware_csv_dir)):
        sample_id = int(file.split('.')[0])
        ip_count = defaultdict(int)
        try:
            df = pd.read_csv(f"{ransomware_csv_dir}/{file}", index_col=0)
            for idx, row in df.iterrows():
                all_sample_ip_count[sample_id][row['src']] += 1
                all_sample_ip_count[sample_id][row['dst']] += 1
        except Exception as e:
            print(f"{sample_id} error!")
            print(e)
    with open(f"{result_dir}/all_sample_ip_count.json", 'w') as f:
        f.write(json.dumps(all_sample_ip_count, indent=4, ensure_ascii=False))
