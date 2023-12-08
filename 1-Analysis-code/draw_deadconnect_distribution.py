import json
import matplotlib.pyplot as plt
from collections import defaultdict


if __name__ == '__main__':
    with open(f'./statistical_result/all_signatures.json', 'r', encoding='utf-8') as f:
        dct = json.loads(f.read())
    record = defaultdict(int)
    for sig in dct:
        if sig.startswith('dead_connect'):
            t = int(sig.split('(')[1].split(' ')[0])
            if t > 100:
                continue
            record[t] = dct[sig][0]
    print(record)
    fig = plt.figure()
    rects = plt.bar(record.keys(), record.values(), color='grey')
    plt.xlabel('dead connect unique time')
    plt.ylabel('sample num')
    plt.bar_label(rects)
    plt.savefig('./figure/deadconnect_distribution.png')
    plt.show()
