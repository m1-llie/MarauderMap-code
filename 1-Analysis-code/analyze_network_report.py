import os
import json
from collections import defaultdict


def filter_domain(domain):
    if domain == 'UBUNTU22-301.local':
        return True

    if domain.find('mozilla') != -1:
        return True

    if domain.find('firefox') != -1:
        return True

    return False


if __name__ == '__main__':
    root_path = "D:\\reports-72-nice-samples"

    domain_count = defaultdict(int)
    domain_2_ip = defaultdict(str)

    for id in os.listdir(root_path):
        print(id)
        if not os.path.exists(f'{root_path}\\{id}\\reports\\report.json'):
            print(f'{id} does not have a report.json!')
            continue
        with open(f'{root_path}\\{id}\\reports\\report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)
        network_info = report['network']

        domain_lst = []
        for d in network_info['domains']:
            if filter_domain(d['domain']):
                continue
            domain_name = d['domain']
            domain_ip = d['ip']
            domain_lst.append(domain_name)
            domain_count[domain_name] += 1
            domain_2_ip[domain_name] = domain_ip

        for d in domain_lst:
            print(f'\t{d} {domain_2_ip[d]}')

    for k, v in sorted(domain_count.items(), key=lambda item: (item[1], domain_2_ip[item[0]]), reverse=True):
        print(k, v, domain_2_ip[k])
