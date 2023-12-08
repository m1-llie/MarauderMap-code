import matplotlib.pyplot as plt
import json


with open(f'./statistical_result/all_signatures.json', 'r') as f:
    dct = json.loads(f.read())

x = []
height = []
for k in dct.keys():
    if k.startswith('dead_connect'):
        unique_time = int(k.split('(')[-1].split(' ')[0])
        if unique_time > 200:
            continue
        print(unique_time, dct[k][0])
        x.append(unique_time)
        height.append(dct[k][0])
print(x, height)
fig = plt.figure()
plt.bar(x=x, height=height)
plt.xlabel('unique time')
plt.ylabel('sample number')
plt.show()
