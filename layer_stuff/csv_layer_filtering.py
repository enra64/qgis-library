from typing import Dict, List, Optional


def __create_filter_string(filters: Dict[str, str]) -> str:
    return "subset=" + " AND ".join(["%22{}%22%20%3D%20'{}'".format(key, value) for key, value in filters.items()])


def create_id_and_direction_filter(user_id: str, direction: str) -> str:
    return __create_filter_string({
        "id": user_id,
        "direction": direction
    })


def create_id_and_time_bracket_filter(user_id: str, time_bracket: str) -> str:
    return __create_filter_string({
        "id": user_id,
        "time_bracket": time_bracket
    })


def create_uri_filter_end(qgis_subset_filter: Optional[str] = None):
    query_filter = "?type=csv" \
                   "&detectTypes=yes" \
                   "&xField=longitude" \
                   "&yField=latitude" \
                   "&crs=EPSG:4326" \
                   "&spatialIndex=no" \
                   "&subsetIndex=no" \
                   "&watchFile=no"

    if qgis_subset_filter:
        query_filter += "&" + qgis_subset_filter
    return query_filter
