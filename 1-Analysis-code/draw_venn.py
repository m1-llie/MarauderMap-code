import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

if __name__ == '__main__':
    with open(f"./statistical_result/all_signatures.json", 'r') as f:
        dct = json.loads(f.read())

    lst = [
        "DGA",
        'dead_connect',
        "network_multiple_direct_ip_connections"
    ]

    lst1 = [
        'network_cnc_http',
        'powershell_download',
        'removes_zoneid_ads'
    ]

    plt.figure()
    g = venn3(subsets=[set(dct[lst1[0]][2]), set(dct[lst1[1]][2]), set(dct[lst1[2]][2])],
              set_labels=('HTTP Download', 'Powershell Download', 'Hide File'),
              alpha=0.6,
              normalize_to=1)
    plt.show()

