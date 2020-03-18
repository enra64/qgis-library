from typing import Dict, List


def filter_id_date(rows: List[Dict], id: str, date: str) -> List[Dict]:
    return [row for row in rows if row["id"] == id and row["date"].startsWith(date)]

