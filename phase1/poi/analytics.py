from typing import Callable, Any

from PyQt5.QtGui import QColor
from qgis.core import QgsDataSourceUri, QgsVectorLayer

from data_processing.heatmap_plugin import create_heatmap
from data_processing.lines import create_line_geometry_postgis, create_line_layer
from database.data_import import get_full_uri, get_pg_connection, get_sql_query_uri, \
    layer_from_database_uri, point_selection_to_ewkt_query
from layer_stuff.basic import add_layer_to_project
from layer_stuff.memory_layer_persistence import persistify_vector_layer
from layer_stuff.symbology import set_linestring_arrow_symbology
from qgis_setup.basic import write_project

persistency_folder = "/home/arne/Documents/git-repos/ubiquitous-systems/generated/"


def __get_geometry_from_city(city_name: str) -> str:
    def query_function(cursor: Any) -> None:
        cursor.execute("SELECT the_geom FROM cities WHERE city_name=%s", (city_name,))

    return __execute_single_cell_result_query(query_function)


def __execute_single_cell_result_query(execute_function: Callable[[Any], None]) -> Any:
    pg_connection = get_pg_connection()
    cursor = pg_connection.cursor()
    execute_function(cursor)
    result = cursor.fetchone()[0]
    cursor.close()
    pg_connection.close()
    return result


def __show_pois(city_name: str, radius: float):
    origin = __get_geometry_from_city(city_name)
    uri = get_full_uri(__distance_where_clause(origin, radius), "pois")
    add_layer_to_project(layer_from_database_uri(uri, "POIs in {}".format(city_name)))


def __show_checkins(city: str, radius: float, user_id: str):
    checkin_point_layer = __get_checkin_layer("Check-Ins of {} in {}".format(user_id, city), city, radius, user_id)
    add_layer_to_project(checkin_point_layer)


def __show_visit_heatmap(city_name: str, radius: float, user_id: str):
    checkin_point_layer = __get_checkin_layer("CPLH", city_name, radius, user_id)
    heatmap_layer = create_heatmap(
        checkin_point_layer,
        persistency_folder,
        "Heatmap of visits from {} in {}".format(user_id, city_name),
        QColor("green")
    )
    add_layer_to_project(heatmap_layer)


def __distance_where_clause(point: str, distance_in_meters: float) -> str:
    return "ST_Distance('{}'::geography, the_geom::geography) < {}".format(point, distance_in_meters)


def __get_checkin_layer(layer_name: str, city_name: str, radius: float, user_id: str) -> QgsVectorLayer:
    origin = __get_geometry_from_city(city_name)
    distance_clause = __distance_where_clause(origin, radius)
    where_clause = "user_id = '{}' AND {}".format(user_id, distance_clause)
    uri = get_full_uri(where_clause, "checkins")
    return layer_from_database_uri(uri, layer_name)


def __show_movement(user_id: str, date: str):
    point_selection_query = \
        "SELECT the_geom FROM checkins WHERE user_id = '{}' AND timestamp::date = '{}' ORDER BY timestamp"
    point_selection_query = point_selection_query.format(user_id, date)
    ewkt_line_query = point_selection_to_ewkt_query(point_selection_query)

    ewkt = __execute_single_cell_result_query(lambda cursor: cursor.execute(ewkt_line_query))
    geometry = create_line_geometry_postgis(ewkt)
    memory_line_layer = create_line_layer(geometry, "Movement of {} on {}".format(user_id, date))
    persistent_line_layer = persistify_vector_layer(persistency_folder, memory_line_layer)
    set_linestring_arrow_symbology(persistent_line_layer)
    add_layer_to_project(persistent_line_layer)


def execute(user_id: str, date: str, city: str):
    radius_meters = 20000
    __show_pois(city, radius_meters)
    __show_checkins(city, radius_meters, user_id)
    __show_movement(user_id, date)
    __show_visit_heatmap(city, radius_meters, user_id)

    outfile = "/home/arne/Documents/git-repos/ubiquitous-systems/generated/POI.qgz"
    write_project(outfile)
