import os
import json
ROOT_PATH=os.getcwd()
file_path=os.path.join(ROOT_PATH,'davidspolk_profile.json')

with open(file_path, encoding="utf-8") as f:
    data = json.load(f)


for record in data:
    all_phones=[]
    phone=record.get('phone')
    if isinstance(phone, str):
        record["phone"] = [phone]
    elif phone is None:
        record["phone"] = []

with open('davidspolk_profile_cleaned.json', 'w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
