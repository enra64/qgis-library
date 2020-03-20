from PyQt5.QtGui import QColor
from qgis.core import QgsDataSourceUri, QgsVectorLayer

from data_processing.heatmap_plugin import create_heatmap
from database.data_import import get_basic_uri, get_full_uri, get_pg_connection, get_sql_query_uri, \
    point_selection_to_line_layer, layer_from_database_uri
from layer_stuff.basic import add_layer_to_project
from qgis_setup.basic import write_project

persistency_folder = "/home/arne/Documents/git-repos/ubiquitous-systems/generated/"


def __get_geometry_from_city(city_name: str) -> str:
    pg_connection = get_pg_connection()
    cursor = pg_connection.cursor()
    cursor.execute("SELECT the_geom FROM cities WHERE city_name=%s", (city_name,))
    geometry = cursor.fetchone()[0]
    cursor.close()
    pg_connection.close()
    return geometry


def __show_pois(city_name: str, radius: float):
    origin = __get_geometry_from_city(city_name)
    where_clause = "ST_Distance(GEOMETRY {}, the_geom) < {};".format(origin, radius)
    uri = get_full_uri(where_clause, "pois")
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


def __get_checkin_layer(layer_name: str, city_name: str, radius: float, user_id: str) -> QgsVectorLayer:
    origin = __get_geometry_from_city(city_name)
    where_clause = "user_id = {} AND ST_Distance(GEOMETRY {}, the_geom) < {};".format(user_id, origin, radius)
    uri = get_full_uri(where_clause, "checkins")
    return layer_from_database_uri(uri, layer_name)


def __show_movement(user_id: str, date: str):
    point_selection_query = \
        "SELECT the_geom FROM checkins WHERE user_id = '{}' AND timestamp::date = '{}' ORDER BY timestamp"
    point_selection_query = point_selection_query.format(user_id, date)
    layer = point_selection_to_line_layer(point_selection_query, "Movement of {} on {}".format(user_id, date))
    add_layer_to_project(layer)


def execute(user_id: str, date: str, city: str):
    radius = 0.02
    __show_pois(city, radius)
    __show_checkins(city, radius, user_id)
    __show_movement(user_id, date)
    __show_visit_heatmap(city, radius, user_id)

    outfile = "/home/arne/Documents/git-repos/ubiquitous-systems/generated/CDR.qgz"
    write_project(outfile)
