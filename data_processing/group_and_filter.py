import csv

from csv_tools.file import read_csv_file
from csv_tools.filter import filter_id_date
from csv_tools.group import group_by


def filter_and_group_calls(csv_file_name: str, out_name: str, user_id: str, date: str):
    """
    Filter csv_file_name to only contain rows from user_id from the specified date.
    Group the remaining rows by the location and get the indexes (i.e. order of visits)
    as a joined string.
    Write to CSV file.
    """
    filtered_calls = filter_id_date(read_csv_file(csv_file_name, delimiter=","), user_id, date)

    filtered_calls.sort(key=lambda _: _["ts"])

    for index, row in enumerate(filtered_calls):
        row["index"] = index

    grouped_calls = group_by(filtered_calls, ["longitude", "latitude"], "index")
    for group in grouped_calls:
        group["index"] = ";".join(group["index"])

    fieldnames = ["longitude", "latitude", "index"]
    with open(out_name, "w") as outfile:
        writer = csv.DictWriter(outfile, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(grouped_calls)


if __name__ == "__main__":
    filter_and_group_calls("/home/arne/Documents/git-repos/ubiquitous-systems/generated/cdr-converted/calls.csv", "generated/test.csv", "24490292", "2007-05-02")