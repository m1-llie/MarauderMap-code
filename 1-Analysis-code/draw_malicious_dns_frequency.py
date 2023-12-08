import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
from special_samples import DGA_samples, rDNS_samples
import pandas as pd
from utils import get_malicious_domain_names
from collections import defaultdict


plt.rcParams['font.sans-serif'] = ['Tahoma']
color = '#AFB0B2'


def make_label(value, pos):
    return f'{int(value)}s'


if __name__ == '__main__':
    malicious_domain_names = set(get_malicious_domain_names())
    # for sample_id in DGA_samples:
    #     df = pd.read_csv(f'./data/ransomware_filtered/{sample_id}.csv', index_col=0)
    #     df = df[df['protocol'] == 'DNS']
    #     df.to_csv(f'G:\\empirical_data\\ransomware_dns\\{sample_id}.csv')
    #     record = defaultdict(int)
    #     for _, row in df.iterrows():
    #         if row['info'].startswith('Standard query response'):
    #             continue
    #         target = row['info'].split(' ')[-1]
    #         if target not in malicious_domain_names:
    #             continue
    #         record[float(row['time'])] += 1
    #     fig = plt.figure()
    #     plt.bar(record.keys(), record.values())
    #     plt.title(f'{sample_id}')
    #     plt.savefig(f'./statistical_result/dns_curve/DGA_{sample_id}.png')
    #     plt.close()
    #
    # for sample_id in rDNS_samples:
    #     df = pd.read_csv(f'./data/ransomware_filtered/{sample_id}.csv', index_col=0)
    #     df = df[df['protocol'] == 'DNS']
    #     df.to_csv(f'G:\\empirical_data\\ransomware_dns\\{sample_id}.csv')
    #     record = defaultdict(int)
    #     for _, row in df.iterrows():
    #         if row['info'].startswith('Standard query response'):
    #             continue
    #         target = row['info'].split(' ')[-1]
    #         if target.find('in-addr') == -1:
    #             continue
    #         record[float(row['time'])] += 1
    #     fig = plt.figure()
    #     plt.bar(record.keys(), record.values())
    #     plt.title(f'{sample_id}')
    #     plt.savefig(f'./statistical_result/dns_curve/rDNS_{sample_id}.png')
    #     plt.close()

    fig = plt.figure(figsize=(6, 3))

    ax = plt.subplot(221)

    df = pd.read_csv(f'./data/ransomware_filtered/{3155}.csv', index_col=0)
    df = df[df['protocol'] == 'DNS']
    record = defaultdict(int)
    for _, row in df.iterrows():
        if row['time'] < 225:
            continue
        if row['info'].startswith('Standard query response'):
            continue
        target = row['info'].split(' ')[-1]
        if target not in malicious_domain_names:
            continue
        record[int(row['time'] / 2) * 2] += 1

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
    plt.bar(record.keys(), record.values(), width=0.9, color=color)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlabel('sample id: 3155')

    ax = plt.subplot(222)

    df = pd.read_csv(f'./data/ransomware_filtered/{4517}.csv', index_col=0)
    df = df[df['protocol'] == 'DNS']

    record = defaultdict(int)
    for _, row in df.iterrows():
        if row['time'] < 240 or row['time'] > 300:
            continue
        if row['info'].startswith('Standard query response'):
            continue
        target = row['info'].split(' ')[-1]
        if target not in malicious_domain_names:
            continue
        record[int(row['time'] / 2) * 2] += 1

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
    plt.bar(record.keys(), record.values(), width=0.6, color=color)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlabel('sample id: 4517')

    ax = plt.subplot(223)
    df = pd.read_csv(f'./data/ransomware_filtered/{900}.csv', index_col=0)
    df = df[df['protocol'] == 'DNS']

    record = defaultdict(int)
    for _, row in df.iterrows():
        if row['info'].startswith('Standard query response'):
            continue
        target = row['info'].split(' ')[-1]
        if target.find('in-addr') == -1:
            continue
        record[int(row['time'] / 2) * 2] += 1

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
    plt.bar(record.keys(), record.values(), width=1.2, color=color)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlabel('sample id: 900')

    ax = plt.subplot(224)
    df = pd.read_csv(f'./data/ransomware_filtered/{7590}.csv', index_col=0)
    df = df[df['protocol'] == 'DNS']

    record = defaultdict(int)
    for _, row in df.iterrows():
        if row['info'].startswith('Standard query response'):
            continue
        target = row['info'].split(' ')[-1]
        if target.find('in-addr') == -1:
            continue
        record[int(row['time'] / 2) * 2] += 1

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
    plt.bar(record.keys(), record.values(), width=1.5, color=color)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlabel('sample id: 7590')

    fig.supylabel('DNS query number')
    fig.tight_layout()
    plt.savefig('./figure/dns_frequency.pdf', dpi=300, bbox_inches='tight')
    # plt.show()
