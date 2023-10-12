# count the number of ransomware samples that reach certain file paths
# output: certain-file-access-sample.json
import json
import glob
from collections import defaultdict
from tqdm import tqdm
import sys


def count_targets_in_files(json_files, target_strings):
    target_counts = defaultdict(int)
    for file in tqdm(json_files, desc="Processing JSON files"):
        with open(file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            files = json_data.get('behavior', {}).get('summary', {}).get('files', [])

        for target in target_strings:
            if any(target in file_path for file_path in files):
                target_counts[target] += 1

    return target_counts


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("need an argument, the folder of runtime logs\n")
        exit()
    input_folder = sys.argv[1]
    output_file = 'certain-file-access-sample.json'
    json_files = glob.glob(input_folder+"/*.json")
    target_strings = [
        "C:\\Windows\\System32",
        "C:\\Windows\\Globalization",
        "C:\\Windows\\apppatch",
        "C:\\Windows\\WindowsShell.Manifest",
        "\\Device\\CNG",
        "C:\\PerfLogs",
        "C:\\$WinREAgent",
        "C:\\$Recycle.Bin",
        "C:\\Program Files",
        "C:\\Windows\\SystemResources",
        "C:\\Users\\anonymous",  # hide the user name for double-blind request
        "C:\\Recovery",
    ]

    target_counts = count_targets_in_files(json_files, target_strings)
    sorted_target_counts = sorted(target_counts.items(), key=lambda x: x[1], reverse=True)
    output = json.dumps(dict(sorted_target_counts), indent=4)

    with open("file_reach_sample_count.json", "w", encoding='utf-8') as f:
        f.write(output)
