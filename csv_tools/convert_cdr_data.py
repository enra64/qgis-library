import csv
from datetime import datetime

from csv_tools.file import read_csv_file


def __get_time_bracket(timestamp: datetime) -> str:
    # 22:00-6:00 9:00-13:00 15:00-18:00;
    if timestamp.hour > 21 or timestamp.hour < 6:
        return "night"
    elif 8 < timestamp.hour < 13:
        return "morning"
    elif 14 < timestamp.hour < 18:
        return "midday"
    else:
        return "other"


def convert():
    csv_file_names = {
        "CT_CDRuser24490292.csv": {"id": "24490292"},
        "CT_CDRuser24750159.csv": {"id": "24750159"},
        "CT_CDRuser24984932.csv": {"id": "24984932"},
        "CT_CDRuser25143787.csv": {"id": "25143787"},
        "CT_CDRuser26024997.csv": {"id": "26024997"},
        "CT_CDRuser32011627.csv": {"id": "32011627"},
    }
    csv_base_path = "/home/arne/Documents/git-repos/ubiquitous-systems/assets/cdr/"
    output_path = "/home/arne/Documents/git-repos/ubiquitous-systems/generated/cdr-converted/"

    all_rows = []
    for csv_file_name, csv_info in csv_file_names.items():
        rows = read_csv_file(csv_base_path + csv_file_name, delimiter=",")
        for row in rows:
            row["id"] = csv_info["id"]
        all_rows.extend(rows)

    for row in all_rows:
        is_incoming = row["id"] == row["originating_id"]

        if is_incoming:
            row["longitude"] = row["orig_longitude"]
            row["latitude"] = row["orig_latitude"]
            row["direction"] = "incoming"
        else:
            if "term_longtitude" in row:
                row["longitude"] = row["term_longtitude"]
            else:
                row["longitude"] = row["term_longitude"]
            row["latitude"] = row["term_latitude"]
            row["direction"] = "outgoing"

        epoch = datetime(1970, 1, 1)
        timestamp = datetime.strptime("{} {}".format(row["date"], row["time"]), "%Y-%m-%d %H:%M:%S")
        row["ts"] = (timestamp - epoch).total_seconds()
        row["time_bracket"] = __get_time_bracket(timestamp)

        del row["originating_id"]
        del row["terminating_id"]
        del row["term_longtitude"]
        del row["term_latitude"]
        del row["orig_longitude"]
        del row["orig_latitude"]

    header = ["id", "longitude", "latitude", "direction", "date", "time", "duration", "time_bracket", "ts"]

    with open(output_path + "calls.csv", "w") as outfile:
        writer = csv.DictWriter(outfile, delimiter=",", fieldnames=header)
        writer.writeheader()
        writer.writerows(all_rows)


if __name__ == "__main__":
    convert()
