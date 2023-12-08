import os
from tqdm import tqdm
import pandas as pd
import shutil
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import json
from config import benign_csv_dir
import numpy as np

plt.rcParams['font.size'] = 8
plt.rcParams['font.sans-serif'] = ['Tahoma']
colors = sns.color_palette('Set2')

title_font_size = 9
p_size = 6
l_size = 7

# record = defaultdict(int)
# for file in tqdm(os.listdir("G:\\empirical_data\\ransomware_network_filtered")):
#     df = pd.read_csv(f'G:\\empirical_data\\ransomware_network_filtered\\{file}', index_col=0)
#     for _, row in df.iterrows():
#         if 'https' in row['info']:
#             record['HTTPS'] += 1
#         elif 'http' in row['info']:
#             record['HTTP'] += 1
#         else:
#             record[row['protocol'].upper()] += 1
#
# del record['DNS']
# s = sum(record.values())
# for k, v in record.items():
#     print(k, v / s * 100)
#
# new_dict = defaultdict(int)
# for k, v in record.items():
#     if v / s < 0.01:
#         new_dict['others'] += v
#     else:
#         new_dict[k] = v
#
# with open(f'./draw_protocol.json', 'w') as f:
#     f.write(json.dumps(new_dict, ensure_ascii=False, indent=4))

fig = plt.figure()

with open(f'./draw_protocol.json', 'r') as f:
    new_dict = json.loads(f.read())

new_dict['Others'] = new_dict['others']
del new_dict['others']
new_dict['Others'] += new_dict['TLSV1.2']
del new_dict['TLSV1.2']

xs = []
labels = []
s = sum(new_dict.values())
for k, v in sorted(new_dict.items(), key=lambda item: item[1], reverse=True):
    xs.append(v)
    labels.append(f'{k}')

color_lst1 = [
    '#6D819C',
    '#B9925F',
    '#BC7E8C',
    '#99A684',
    '#A187A1',
    '#AD8978'
]

plt.subplot(121)
patches, l_text, p_text = plt.pie(x=xs,
        labels=labels,
        autopct='%.0f%%',
        pctdistance=0.88,
        textprops={'fontsize': 8, 'weight': 'medium'},
        colors=colors,
        startangle=0)
plt.title('Ransomware', fontdict={'fontsize': title_font_size, 'weight': 'semibold'}, y=-0.1)

for t in l_text:
    t.set_size(l_size)
    t.set_weight('bold')
for t in p_text:
    value = int(t.get_text().split('%')[0])
    if value < 3:
        # t.set_visible(False)
        t.set_size(3)
    else:
        t.set_size(p_size)

# record = defaultdict(int)
# for file in tqdm(os.listdir(benign_csv_dir)):
#     try:
#         protocol_usage = defaultdict(lambda: defaultdict(int))
#         sample_id = int(file.split('.')[0])
#
#         df = pd.read_csv(f'{benign_csv_dir}/{file}', index_col=0)
#
#         for idx, row in df.iterrows():
#             record[row['protocol']] += 1
#     except:
#         print(f"{file} error!")
#
# del record['DNS']
# s = sum(record.values())
# new_dict = defaultdict(int)
# for k, v in record.items():
#     if v / s < 0.01:
#         new_dict['others'] += v
#     else:
#         new_dict[k] = v
# with open('./draw_protocol_benign.json', 'w') as f:
#     f.write(json.dumps(new_dict, ensure_ascii=False, indent=4))

with open('./draw_protocol_benign.json', 'r') as f:
    record = json.loads(f.read())

record['Others'] = record['others']
del record['others']

xs = []
labels = []
for k, v in sorted(record.items(), key=lambda item: item[1], reverse=True):
    if k != 'Others':
        xs.append(v)
        labels.append(k)
xs.append(record['Others'])
labels.append('Others')

plt.subplot(122)
color_lst2 = [
    '#1E88E5',
    '#43A047',
    '#FFEB3B',
    '#E53935',
    '#8E24AA',
    '#00ACC1',
    '#FFB300',
    '#EC407A',
    '#795548',
    '#546E7A',
    '#5C6BC0',
    '#66BB6A',
    '#D4E157'
]
patches, l_text, p_text = plt.pie(x=xs,
        autopct='%.0f%%',
        labels=labels,
        pctdistance=0.88,
        textprops={'fontsize': 8, 'weight': 'medium'},
        colors=colors)

for t in l_text:
    t.set_size(l_size)
    t.set_weight('bold')
# l_text[-2].set_label_coords(1.0408, -0.34)
l_text[-2].set_y(-0.32)
for t in p_text:
    value = int(t.get_text().split('%')[0])
    if value < 3:
        # t.set_visible(False)
        t.set_size(3)
    else:
        t.set_size(p_size)

plt.title('Benign Programs', fontdict={'fontsize': title_font_size, 'weight': 'bold'}, y=-0.1)

plt.subplots_adjust(wspace=0.6)
plt.savefig('./figure/protocol_used.pdf', bbox_inches='tight')
# plt.show()
