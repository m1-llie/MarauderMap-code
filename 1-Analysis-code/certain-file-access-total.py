# count file access - total
# output: certain_file_access_total.json
import json
from collections import defaultdict
from tqdm import tqdm
import sys


def count_targets(input_data, target_strings):
    target_counts = defaultdict(int)
    for source, count in tqdm(input_data.items(), desc="Processing"):
        for target in target_strings:
            if target in source:
                target_counts[target] += count
                break
    return target_counts


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("need an argument, the file path of count_files.json\n")
        exit()
    input_file = sys.argv[1]
    output_file = "./certain_file_access_total.json"

    with open(input_file, "r", encoding="utf-8") as f:
        input_data = json.load(f)

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

    target_counts = count_targets(input_data, target_strings)
    sorted_target_counts = sorted(target_counts.items(), key=lambda x: x[1], reverse=True)
    output = json.dumps(dict(sorted_target_counts), indent=4)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)
