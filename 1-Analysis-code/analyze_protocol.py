from config import ransomware_csv_dir, benign_csv_dir, result_dir, ransomware1888_id, ransomware1888_result_dir
from utils import is_clean_domain
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import os
import json
from tqdm import tqdm
import seaborn as sns


def draw_pie(dct, title="", save_path=None, pct=0.05, show=False):
    total = sum(dct.values())
    draw_dct = defaultdict(int)
    for k, v in dct.items():
        if v < total * pct:
            draw_dct['others'] += v
        else:
            draw_dct[k] = v
    plt.figure()
    plt.pie(x=draw_dct.values(), labels=draw_dct.keys(), autopct='%.1f%%')
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
    plt.close()


def draw_usage(dct, title="", save_path=None, show=False):
    plt.figure()
    legends = []
    for protocol in dct:
        # plt.plot(dct[protocol].keys(), dct[protocol].values())
        # sns.distplot(dct[protocol].values())
        plt.bar(dct[protocol].keys(), dct[protocol].values(), alpha=0.4)
        legends.append(protocol)
    plt.title(title)
    plt.legend(legends, loc='upper right')
    plt.xlabel('time')
    plt.ylabel('count')
    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
    plt.close()


if __name__ == '__main__':
    protocol_count = defaultdict(int)
    protocol_port_count = defaultdict(int)

    for file in os.listdir(ransomware_csv_dir):
        print(file)
        protocol_usage = defaultdict(lambda: defaultdict(int))
        sample_id = int(file.split('.')[0])

        df = pd.read_csv(f'{ransomware_csv_dir}/{file}', index_col=0)

        for idx, row in df.iterrows():
            if is_clean_domain(row['src']) or is_clean_domain(row['dst']) or (row['protocol'] == 'DNS' and is_clean_domain(row['info'].split(' ')[-1])):
                continue
            if row['protocol'] == 'HTTP':
                print(row['info'])
            protocol_count[row['protocol']] += 1
            protocol_port_count[f"{row['protocol']}:{row['port']}"] += 1
            protocol_usage[row['protocol']][int(row['time'])] += 1

        if not os.path.exists(f"./{ransomware1888_result_dir}/usage_curve"):
            os.makedirs(f"./{ransomware1888_result_dir}/usage_curve")
        draw_usage(protocol_usage, title=f"{sample_id} protocol usage", save_path=f"./{ransomware1888_result_dir}/usage_curve/{sample_id}.png", show=False)

    with open(f'{ransomware1888_result_dir}/ransomware_protocol_count.json', 'w') as f:
        f.write(json.dumps(protocol_count, indent=4, ensure_ascii=False))

    with open(f'{ransomware1888_result_dir}/ransomware_protocol_port_count.json', 'w') as f:
        f.write(json.dumps(protocol_port_count, indent=4, ensure_ascii=False))

    draw_pie(protocol_count, "ransomware protocol count", f"{ransomware1888_result_dir}/ransomware_protocol_count.png", show=True, pct=0.01)
    draw_pie(protocol_port_count, "ransomware protocol port count", f"{ransomware1888_result_dir}/ransomware_protocol_port_count.png", show=True, pct=0.01)

    # protocol_count = defaultdict(int)
    # protocol_port_count = defaultdict(int)
    #
    # for file in tqdm(os.listdir(benign_csv_dir)):
    #     try:
    #         protocol_usage = defaultdict(lambda: defaultdict(int))
    #         sample_id = int(file.split('.')[0])
    #
    #         df = pd.read_csv(f'{benign_csv_dir}/{file}', index_col=0)
    #
    #         for idx, row in df.iterrows():
    #             protocol_count[row['protocol']] += 1
    #             protocol_port_count[f"{row['protocol']}:{row['port']}"] += 1
    #             protocol_usage[row['protocol']][int(row['time'])] += 1
    #     except:
    #         print(f"{sample_id} error!")
    #
    # with open(f'{result_dir}/benign_protocol_count.json', 'w') as f:
    #     f.write(json.dumps(protocol_count, indent=4, ensure_ascii=False))
    #
    # with open(f'{result_dir}/benign_protocol_port_count.json', 'w') as f:
    #     f.write(json.dumps(protocol_port_count, indent=4, ensure_ascii=False))
    #
    # draw_pie(protocol_count, "benign protocol count", f"{result_dir}/benign_protocol_count.png", show=True,
    #          pct=0.01)
    # draw_pie(protocol_port_count, "benign protocol port count", f"{result_dir}/benign_protocol_port_count.png",
    #          show=True, pct=0.01)
