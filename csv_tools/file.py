import csv
import re
from typing import Union, Dict, List

from qgis.core import QgsVectorLayer


def filename_to_uri(filename: str) -> str:
    return "file://" + filename


def read_csv_file(filename: str) -> List[Dict]:
    with open(filename, "r") as file:
        reader = csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        return list(reader)


def guess_layer_name(file_uri: str):
    if match := re.search(".*/(.*).csv\\?.*", file_uri, re.IGNORECASE):
        return match.group(1)
    return "hmmm"
