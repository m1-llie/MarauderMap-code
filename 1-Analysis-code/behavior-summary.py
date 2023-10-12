# obtain information about files，keys and commands
import json
import os
from collections import defaultdict
from tqdm import tqdm
import sys


def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    summary = data['behavior']['summary']
    return summary


def count_summary_items(summary_items):
    summary_count = defaultdict(int)
    for item in summary_items:
        summary_count[item] += 1
    
    return summary_count

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("need an argument, the folder of runtime logs json files\n")
        exit()
    input_folder = sys.argv[1]
    output_folder = './analysis-output' 

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # keywords in the runtime logs
    summary_keys = [
        "files", "read_files", "write_files", "delete_files", "keys", "read_keys", "write_keys",
        "delete_keys", "executed_commands", "resolved_apis", "mutexes", "created_services", "started_services"
    ]

    all_files_summary_counts = {key: defaultdict(int) for key in summary_keys}

    for file_name in tqdm(os.listdir(input_folder)):
        file_path = os.path.join(input_folder, file_name)
        if not file_path.endswith('.json'):
            continue

        summary = process_json_file(file_path)

        for key in summary_keys:
            if key in summary:
                summary_count = count_summary_items(summary[key])

                for item, count in summary_count.items():
                    all_files_summary_counts[key][item] += count

    for key in summary_keys:
        output_file = os.path.join(output_folder, f"count_{key}.json")
        sorted_counts = dict(sorted(all_files_summary_counts[key].items(), key=lambda x: x[1], reverse=True))
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(sorted_counts, outfile, ensure_ascii=False, indent=4)
