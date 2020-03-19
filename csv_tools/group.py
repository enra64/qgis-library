from collections import defaultdict
from typing import List, Dict


def group_by(rows: List[Dict], group_key_fields: List[str], group_value_field: str) -> List[Dict]:
    groups = defaultdict(list)

    for row in rows:
        key = "|".join([row[key] for key in group_key_fields])
        groups[key].append(row[group_value_field])

    result = []
    for key, values in groups.items():
        result_row_dict = {}

        keys = zip(group_key_fields, key.split("|"))
        for key, value in keys:
            result_row_dict[key] = value
        result_row_dict[group_value_field] = value
        result.append(result_row_dict)

    return result
