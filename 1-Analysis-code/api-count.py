# calculate [behavior-->processes-->api] count of each API
# output: 'api_individual.json', 'api_conclude.json', 'api_all.json', 'api_sequences.json'
import json
import os
from collections import defaultdict
from tqdm import tqdm
from chardet.universaldetector import UniversalDetector
import sys


def detect_file_encoding(file_path):
    detector = UniversalDetector()
    with open(file_path, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']


def process_json_file(file_path, api_count_global):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except UnicodeDecodeError:
        try:
            encoding = detect_file_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as file:
                data = json.load(file)
        except Exception as e:
            print(f"cannot deal with {file_path}: {e}")
            return False, False

    api_count_local = defaultdict(int)    
    api_sequences = []  

    for id in data['behavior']['processes']:
        api_sequence = []
        for id2 in id['calls']:
            api = id2['api']
            api_count_local[api] += 1
            api_count_global[api] += 1
            api_sequence.append(api)
        api_sequences.append(api_sequence)

    return api_count_local, api_sequences


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("need an argument, the folder of runtime json files\n")
        exit()
    input_folder = sys.argv[1]
    # API call count
    output_file_individual = 'api_individual.json'
    output_file_conclude = 'api_conclude.json'
    output_file_all = 'api_all.json'
    api_count_global = defaultdict(int)
    api_counts_per_file = {}
    # API call chain
    output_file = 'api_sequences.json'
    api_sequences_per_file = {}

    json_files = [file for file in os.listdir(input_folder) if file.endswith('.json')]

    for json_file in tqdm(json_files, desc="Processing API information in JSON files"):
        file_path = os.path.join(input_folder, json_file)
        result = process_json_file(file_path, api_count_global)
        if result:   
            # API call count and call chain
            api_count_local, api_sequences = result
            api_counts_per_file[json_file] = api_count_local
            api_sequences_per_file[json_file] = api_sequences

    api_count_global = dict(sorted(api_count_global.items(), key=lambda x: x[1], reverse=True))

    combined_api_counts = {
        "api_count_total": api_count_global,
        "api_counts_per_file": api_counts_per_file
    }

    with open(output_file_all, 'w', encoding='utf-8') as outfile:
        json.dump(combined_api_counts, outfile, ensure_ascii=False, indent=4)

    with open(output_file_individual, 'w', encoding='utf-8') as outfile:
        json.dump(api_counts_per_file, outfile, ensure_ascii=False, indent=4)

    with open(output_file_conclude, 'w', encoding='utf-8') as outfile:
        json.dump(api_count_global, outfile, ensure_ascii=False, indent=4)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(api_sequences_per_file, outfile, ensure_ascii=False, indent=4)
