from qgis.core import QgsDataSourceUri, QgsVectorLayer

from database.data_import import get_basic_uri, get_full_uri, get_pg_connection
from layer_stuff.basic import add_layer_to_project


def __get_geometry_from_city(city_name: str) -> str:
    pg_connection = get_pg_connection()
    cursor = pg_connection.cursor()
    cursor.execute("SELECT the_geom FROM cities WHERE city_name=%s", city_name)
    return cursor.fetchone()["the_geom"]

def __show_pois(layer_name: str, city_name: str, radius: float):
    origin = __get_geometry_from_city(city_name)
    where_clause = "ST_Distance(GEOMETRY {}, the_geom) < {};".format(origin, radius)
    uri = get_full_uri(where_clause, "pois")
    layer = QgsVectorLayer(uri.uri(False), layer_name, "postgres")
    add_layer_to_project(layer)


def __show_checkins(layer_name: str, city_name: str, radius: float, user_id: str):
    origin = __get_geometry_from_city(city_name)
    where_clause = "user_id = {} AND ST_Distance(GEOMETRY {}, the_geom) < {};".format(user_id, origin, radius)
    uri = get_full_uri(where_clause, "checkins")
    layer = QgsVectorLayer(uri.uri(False), layer_name, "postgres")
    add_layer_to_project(layer)


def __show_movement(user_id: str, date: str):
    pass


def __show_visit_heatmap(user_id: str):
    pass
