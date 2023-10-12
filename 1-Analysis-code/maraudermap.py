# towards better defense, implement the propotype of proposed detectors
# output: output-1.json, output-2.json, output-maraudermap.json, marauder-detection.log
import json
import os
import sys
from collections import defaultdict
from tqdm import tqdm
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
from math import ceil
from datetime import datetime, timedelta
import logging


def find_partial_subsequence(seq, subseq, min_length=2):
    if len(subseq) < min_length:
        return []

    partial_matches = []

    for i in range(len(seq)):
        match_count = 0
        for j in range(len(subseq)):
            if i + j < len(seq) and seq[i + j] == subseq[j]:
                match_count += 1
            else:
                break
        if match_count >= min_length:
            partial_matches.append((tuple(seq[i:i + match_count]), i))

    return partial_matches


def merge_subsequences(subsequences):
    merged_subseq = defaultdict(int)
    for subseq, count in subsequences.items():
        merged = False
        for merged_key in list(merged_subseq.keys()):
            if merged_key[-1] == subseq[0] and merged_key != subseq:
                merged_key_new = merged_key + subseq[1:]
                min_count = min(merged_subseq[merged_key], count)
                diff_count = abs(merged_subseq[merged_key] - count)
                merged_subseq[merged_key_new] = min_count
                merged_subseq[merged_key] = diff_count
                merged = True
                break
            elif merged_key[0] == subseq[-1] and merged_key != subseq:
                merged_key_new = subseq[:-1] + merged_key
                min_count = min(merged_subseq[merged_key], count)
                diff_count = abs(merged_subseq[merged_key] - count)
                merged_subseq[merged_key_new] = min_count
                merged_subseq[merged_key] = diff_count
                merged = True
                break
        if not merged:
            merged_subseq[subseq] = count

    return merged_subseq


def final_subsequence_chain(seq, subseq, min_length):
    partial_matches = find_partial_subsequence(seq, subseq, min_length)
    if not partial_matches:
        return False

    subsequences_counts = defaultdict(int)
    for subseq, start_index in partial_matches:
        subsequences_counts[subseq] += 1

    merged_subsequences = merge_subsequences(subsequences_counts)

    longest_match = max(merged_subsequences, key=len)

    for subseq, start_index in partial_matches:
        if subseq == longest_match:
            return start_index

    return False


def extract_info(data):
    info = {}
    inject_methods = [
        "Thread execution hijacking",
        "Classic DLL injection",
        "Apc injection",
        "Process hollowing",
        "Process doppelganging",
        "Systemwide hooks injection"
    ]

    encryption_methods = [
        "Overwrite",
        "Delete and rewrite",
        "Smash and rewrite"
    ]

    inject_method_sequences = {
        "Thread execution hijacking": ['NtOpenProcess', 'NtAllocateVirtualMemory', 'NtAllocateVirtualMemoryEx', 'WriteProcessMemory', 'CreateThread', 'NtCreateThreadEx', 'NtResumeThread'],
        "Classic DLL injection": ['NtOpenProcess', 'NtAllocateVirtualMemory', 'NtAllocateVirtualMemoryEx', 'NtWriteVirtualMemory', 'WriteProcessMemory', 'CreateRemoteThread'],
        "Apc injection": ['CreateToolhelp32Snapshot', 'Process32FirstW', 'Process32NextW', 'NtOpenProcess', 'NtAllocateVirtualMemory', 'NtAllocateVirtualMemoryEx', 'NtSuspendThread', 'WriteProcessMemory', 'NtQueueApcThread'],
        "Process hollowing": ['ReadProcessMemory', 'NtUnmapViewOfSection', 'NtUnmapViewOfSectionEx', 'WriteProcessMemory', 'VirtualProtectEx', 'NtSetContextThread', 'NtResumeThread'],
        "Process doppelganging": ['NtCreateTransaction', 'NtCreateFile', 'NtWriteFile', 'NtCreateSection', 'NtCreateProcessEx', 'CreateThread', 'NtCreateThreadEx'],
        "Systemwide hooks injection": ['SetWindowsHookExW', 'SetWindowsHookExA', 'GetAsyncKeyState']
    }
    
    encryption_method_sequences = {
        "Overwrite": ['NtOpenProcess', 'ReadProcessMemory', 'NtWriteFile', 'NtClose'], 
        "Delete and rewrite": ['NtCreateFile', 'NtReadFile', 'DeleteFileA', 'NtCreateFile', 'NtWriteFile'],
        "Smash and rewrite": ['NtCreateFile', 'NtReadFile', 'NtCreateFile', 'NtWriteFile']
    }


    registry_apis = [
        'NtDeleteValueKey',
        'NtSetValueKey',
        'RegDeleteValueA',
        'RegSetValueExA',
        'RegCreateKeyExA',
        'RegCreateKeyExW',
        'RegDeleteKeyW',
        'RegDeleteKeyA',
        'RegDeleteValue'
    ]
    
    processes = data['behavior']['processes']
    if processes:
        earliest_timestamp = datetime.max
        latest_timestamp = datetime.min

        inject_timestamps = []
        registry_timestamps = []
        encryption_timestamps = []
        user_dir_timestamps = []

        inject_method_occurrence = {method: False for method in inject_methods}
        encryption_method_occurrence = {method: False for method in encryption_methods}
        registry_count = 0
        user_dir_count = 0

        for process in processes:
            calls = process['calls']
            api_sequence = [call['api'] for call in calls]   

            for call in calls:
                api = call['api']
                category = call['category']
                timestamp_str = call['timestamp']
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")

                if timestamp < earliest_timestamp:
                    earliest_timestamp = timestamp

                if timestamp > latest_timestamp:
                    latest_timestamp = timestamp

                for method, sequence in inject_method_sequences.items():
                    if api == sequence[0] and not inject_method_occurrence[method]:
                        start_index = final_subsequence_chain(api_sequence, sequence, 3) 
                        if start_index is not None:
                            inject_method_occurrence[method] = True
                            inject_timestamps.append({"method": method, "timestamp": calls[start_index]["timestamp"]})

                for method, sequence in encryption_method_sequences.items():
                    if api == sequence[0] and not encryption_method_occurrence[method]:
                        start_index = final_subsequence_chain(api_sequence, sequence, 4)  
                        if start_index is not None:
                            encryption_method_occurrence[method] = True
                            encryption_timestamps.append({"method": method, "timestamp": calls[start_index]["timestamp"]})

                if api in registry_apis:
                    registry_count += 1
                    registry_timestamps.append({"api": api, "timestamp": timestamp})

                if category == "filesystem":
                    for argument in call['arguments']:
                        value = argument['value']
                        if isinstance(value, str) and value.startswith("C:\\Users"):  
                            user_dir_count += 1
                            user_dir_timestamps.append({"value": value, "timestamp": timestamp})


        info["process_start_time"] = earliest_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        info["process_end_time"] = latest_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

        if registry_count > 0:
            middle_index = registry_count // 10 * 3
            info["registry_timestamp"] = registry_timestamps[middle_index]["timestamp"].strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

        if user_dir_count > 0:
            middle_index = user_dir_count // 10 * 5
            info["user_dir_timestamp"] = user_dir_timestamps[middle_index]["timestamp"].strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

        info["inject_timestamps"] = inject_timestamps
        info["encryption_timestamps"] = encryption_timestamps 

    return info


def extract_info_single_file(file_name, input_folder):
    file_path = os.path.join(input_folder, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    info = extract_info(data)
    return file_name, info


def process_step_1(input_folder, output_file_1, num_workers=8, batch_size=1000):
    json_files_to_process = [file_name for file_name in os.listdir(input_folder) if file_name.endswith('.json')]

    output_data = {}
    total_batches = ceil(len(json_files_to_process) / batch_size)

    for batch in range(total_batches):
        batch_start = batch * batch_size
        batch_end = min((batch + 1) * batch_size, len(json_files_to_process))
        batch_files = json_files_to_process[batch_start:batch_end]

        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = {executor.submit(extract_info_single_file, file_name, input_folder): file_name for file_name in batch_files}

            for future in tqdm(concurrent.futures.as_completed(futures), desc="Step 1 processing", total=len(batch_files)):
                file_name, info = future.result()
                output_data[file_name] = info
    
    with open(output_file_1, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)


def time_diff_ms(start, end):
    start_datetime = datetime.strptime(start, "%Y-%m-%d %H:%M:%S,%f")
    end_datetime = datetime.strptime(end, "%Y-%m-%d %H:%M:%S,%f")
    diff = end_datetime - start_datetime
    return diff.total_seconds() * 1000


def compute_time_single_sample(sample):
    if "process_start_time" not in sample:
        return None

    result = {}

    process_start_time = sample["process_start_time"]
    process_end_time = sample["process_end_time"]
    process_duration = time_diff_ms(process_start_time, process_end_time)

    encryption_timestamps = sample["encryption_timestamps"]
    if not encryption_timestamps:
        return None
    encryption_time = max([datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S,%f") for t in encryption_timestamps])

    for encryption_method in ["Delete and rewrite", "Overwrite", "Smash and rewrite"]:
        encrypt_method_lower = encryption_method.replace(" ", "").lower()
        method_data = next((t for t in encryption_timestamps if t["method"] == encryption_method), None)

        if method_data:
            timestamp = method_data["timestamp"]
            result[f"can_detect_{encrypt_method_lower}"] = True
            detect_time = time_diff_ms(process_start_time, timestamp)
            result[f"detection_time_{encrypt_method_lower}"] = detect_time if detect_time >= 0 else None
            percent_time = round(detect_time / process_duration * 100, 2) if process_duration else None
            result[f"detection_time_percent_{encrypt_method_lower}"] = percent_time
        else:
            result[f"can_detect_{encrypt_method_lower}"] = False
            result[f"detection_time_{encrypt_method_lower}"] = None
            result[f"detection_time_percent_{encrypt_method_lower}"] = None

    inject_timestamps = sample["inject_timestamps"]
    earliest_inject_timestamp = min([datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S,%f") for t in inject_timestamps], default=None)
    result["encryption_time"] = encryption_time.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

    for detection_key, timestamp_key in [("detect_injection", "inject_timestamps"),
                                         ("detect_registry", "registry_timestamp"),
                                         ("detect_file_scan", "user_dir_timestamp")]:

        if timestamp_key not in sample or not sample[timestamp_key]:
            result[f"can_{detection_key}_before_encryption"] = None
            result[f"{detection_key}_time"] = None
            continue

        timestamps = sample[timestamp_key]
        earliest_timestamp = None
        if detection_key == "detect_injection":
            earliest_timestamp = earliest_inject_timestamp
        elif isinstance(timestamps, str):
            earliest_timestamp = datetime.strptime(timestamps, "%Y-%m-%d %H:%M:%S,%f")
        elif isinstance(timestamps, list):
            earliest_timestamp = min([datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S,%f") for t in timestamps], default=None)

        if earliest_timestamp:
            result[f"can_{detection_key}_before_encryption"] = earliest_timestamp < encryption_time
            detection_time = time_diff_ms(process_start_time, earliest_timestamp.strftime("%Y-%m-%d %H:%M:%S,%f"))
            result[f"{detection_key}_time"] = detection_time if detection_time >= 0 else None
        else:
            result[f"can_{detection_key}_before_encryption"] = None
            result[f"{detection_key}_time"] = None

    return result


def process_step_2(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    results = {}
    for sample_key, sample_data in tqdm(data.items(), desc="Step 2 processing"):
        processed_sample = compute_time_single_sample(sample_data)  
        if processed_sample is not None:  
            results[sample_key] = processed_sample 

    return results


def process_step_3(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    for sample in data.values():
        detect_encrypt_pattern = (
            sample["can_detect_deleteandrewrite"]
            or sample["can_detect_overwrite"]
            or sample["can_detect_smashandrewrite"]
        )
        sample["detect_encrypt_pattern"] = detect_encrypt_pattern
        
        detect_sensitive_behavior = (
            sample["can_detect_injection_before_encryption"]
            or sample["can_detect_registry_before_encryption"]
            or sample["can_detect_file_scan_before_encryption"]
        )
        sample["detect_sensitive_behavior"] = detect_sensitive_behavior

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)


def final_result_logging(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    arr_ok = []
    arr_ransom = []
    for key, value in data.items():
        if (value["detect_encrypt_pattern"] or value["detect_sensitive_behavior"]):
            arr_ransom.append(key)
        else:
            arr_ok.append(key)
   
    logging.info("ransomware:")
    logging.info(arr_ransom)
    logging.info("benign program:")
    logging.info(arr_ok)

    logging.info("")
    logging.info(data)

    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("need an argument, the folder of json report files\n")
        exit()
    input_folder = sys.argv[1]
    output_file_1 = "./output-1.json"
    output_file_2 = "./output-2.json"
    output_file_3 = "./output-maraudermap.json"
    
    process_step_1(input_folder, output_file_1)
    
    results = process_step_2(output_file_1)
    with open(output_file_2, "w") as f:
        json.dump(results, f, indent=4)

    process_step_3(output_file_2, output_file_3)

    logging.basicConfig(filename='marauder-detection.log', level=logging.INFO, format='%(message)s')
    final_result_logging(output_file_3)
