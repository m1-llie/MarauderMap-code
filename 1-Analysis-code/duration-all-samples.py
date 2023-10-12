# To calculate the running duration of all samples.
# output: duration-all-samples.json
import os
import json
from datetime import datetime
from collections import defaultdict
from tqdm import tqdm
import sys


def calculate_duration(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    try:
        start_timestamp = data['behavior']['processes'][0]['first_seen']
        end_timestamp = data['behavior']['processes'][-1]['first_seen']
    except IndexError:
        return None

    start_datetime = datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S,%f")
    end_datetime = datetime.strptime(end_timestamp, "%Y-%m-%d %H:%M:%S,%f")

    duration = (end_datetime - start_datetime).total_seconds()

    return duration

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("need an argument, the folder of runtime logs\n")
        exit()
    input_folder = sys.argv[1]
    output_file = "duration-all-samples.json"

    durations = []
    duration_count = defaultdict(int)
    file_durations = []

    json_files = [file_name for file_name in os.listdir(input_folder) if file_name.endswith('.json')]

    for file_name in tqdm(os.listdir(input_folder), desc="Processing files"):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_folder, file_name)
            duration = calculate_duration(file_path)
            if duration is not None:
                durations.append(duration)
                duration_category = (1 + int(duration // 60)) * 60
                duration_count[duration_category] += 1
                file_durations.append({"file_name": file_name, "duration": duration})

    sorted_duration_count = dict(sorted(duration_count.items()))
    sorted_file_durations = sorted(file_durations, key=lambda x: x["duration"], reverse=True)
    
    duration_stats = {
        "total_files": len(json_files),
        "samples_with_processes": len(durations),  
        "duration_count": sorted_duration_count,
        "file_durations": sorted_file_durations
    }

    with open(output_file, 'w') as outfile:
        json.dump(duration_stats, outfile, indent=4)
