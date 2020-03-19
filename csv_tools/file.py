import csv
import re
from typing import Dict, List


def filename_to_uri(filename: str) -> str:
    return "file://" + filename


def read_csv_file(filename: str, delimiter: str) -> List[Dict]:
    if filename.startswith("file://"):
        raise Exception("Ya dumbass that's an URI not a filename!")

    with open(filename, "r") as file:
        reader = csv.DictReader(file, delimiter=delimiter, quoting=csv.QUOTE_NONE)
        return list(reader)


def guess_layer_name(file_uri: str):
    if match := re.search(".*/(.*).csv\\?.*", file_uri, re.IGNORECASE):
        return match.group(1)
    return "hmmm"
