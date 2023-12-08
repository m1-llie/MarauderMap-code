import os
import json
from tqdm import tqdm
from collections import defaultdict
from config import result_dir


if __name__ == '__main__':
    root_dir = "D:\\reportjson-all-in-all"

    signatures = defaultdict(lambda: [0, []])

    for file in tqdm(os.listdir(root_dir)):
        try:
            sample_id = file.split('.')[0]
            json_path = f"{root_dir}\\{file}"
            if not os.path.exists(json_path):
                continue
            with open(f"{root_dir}\\{file}", "r", encoding='UTF-8') as f:
                dct = json.loads(f.read())
                for sig in dct['signatures']:
                    s = sig['name'] + ':' + sig['description']
                    signatures[s][0] += 1
                    signatures[s][1].append(sample_id)
        except:
            print(f"{file} error")
    with open(f"{result_dir}/all_signatures.json", 'w') as f:
        f.write(json.dumps(signatures, indent=4, ensure_ascii=False))

    # with open(f'{result_dir}/all_suricata.json', 'w') as f:
    #     f.write(json.dumps(suricata, indent=4, ensure_ascii=False))
