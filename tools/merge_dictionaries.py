from typing import List
from collections import defaultdict

def merge_dictionaries_by_key(data: List[dict], key) -> List[dict]:
    """A small function to merge 2 dictionaries together by key
    """
    fused_data = defaultdict(dict)
    for item in data:
        item_id = item.get(key)
        fused_data[item_id] = merge_dicts(fused_data[item_id], item)
    return list(fused_data.values())

def merge_dicts(dict1, dict2):
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged
