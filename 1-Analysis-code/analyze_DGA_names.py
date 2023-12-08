from collections import defaultdict
import numpy as np
import json
from utils import is_clean_domain
import os
from tqdm import tqdm


def calculate_entropy_of_domain_name(domain_name):
    dct = defaultdict(int)
    s = domain_name.split('.')[0]
    for i in range(len(s)):
        dct[s[i]] += 1
    total = len(s)
    res = 0
    for k, v in dct.items():
        p = v / total
        res -= p * np.log2(p)
    return res


def calculate_maximum_sequential_consonant(domain_name):
    domain_name = domain_name.lower()
    consonants = "bcdfghjklmnpqrstvwxyz"
    max_count = 0
    current_count = 0
    for char in domain_name:
        if char in consonants:
            current_count += 1
            max_count = max(max_count, current_count)
        else:
            current_count = 0
    return max_count


def calculate_maximum_sequential_vowel(domain_name):
    domain_name = domain_name.lower()
    vowels = "aeiou"
    max_count = 0
    current_count = 0
    for char in domain_name:
        if char in vowels:
            current_count += 1
            max_count = max(max_count, current_count)
        else:
            current_count = 0
    return max_count


if __name__ == '__main__':
    malicious_domains = set()
    benign_domains = set()

    with open('./statistical_result/DGA1.json', 'r', encoding='utf-8') as f:
        DGA_json = json.loads(f.read())

    for sample_id, lst in DGA_json.items():
        for domain_name in lst:
            if is_clean_domain(domain_name):
                continue
            malicious_domains.add(domain_name)

    with open(f'./statistical_result/malicious_domains.txt', 'w') as f:
        for d in malicious_domains:
            f.write(f'{d}\n')

    malicious_domain_entropy = []
    benign_domain_entropy = []
    for d in malicious_domains:
        malicious_domain_entropy.append(calculate_entropy_of_domain_name(d))
    for d in benign_domains:
        benign_domain_entropy.append(calculate_entropy_of_domain_name(d))
    print(sum(malicious_domain_entropy) / len(malicious_domain_entropy))
    print(sum(benign_domain_entropy) / len(benign_domain_entropy))

    malicious_max_seq_consonant = []
    benign_max_seq_consonant = []
    for d in malicious_domains:
        malicious_max_seq_consonant.append(calculate_maximum_sequential_consonant(d))
    for d in benign_domains:
        benign_max_seq_consonant.append(calculate_maximum_sequential_consonant(d))
    print(sum(malicious_max_seq_consonant) / len(malicious_max_seq_consonant))
    print(sum(benign_max_seq_consonant) / len(benign_max_seq_consonant))

    malicious_max_seq_vowel = []
    benign_max_seq_vowel = []
    for d in malicious_domains:
        malicious_max_seq_vowel.append(calculate_maximum_sequential_vowel(d))
    for d in benign_domains:
        benign_max_seq_vowel.append(calculate_maximum_sequential_vowel(d))
    print(sum(malicious_max_seq_vowel) / len(malicious_max_seq_vowel))
    print(sum(benign_max_seq_vowel) / len(benign_max_seq_vowel))

