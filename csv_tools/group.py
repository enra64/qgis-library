from collections import defaultdict
from typing import List, Dict


def group_by(rows: List[Dict], group_key_fields: List[str], group_value_field: str) -> List[Dict]:
    groups = defaultdict(list)

    for row in rows:
        key = "|".join([row[key] for key in group_key_fields])
        groups[key].append(str(row[group_value_field]))

    result = []
    for key, values in groups.items():
        result_row_dict = dict(zip(group_key_fields, key.split("|")))
        result_row_dict[group_value_field] = values
        result.append(result_row_dict)

    return result
