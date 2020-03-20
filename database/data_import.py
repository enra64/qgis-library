import psycopg2
from qgis.core import QgsDataSourceUri, QgsVectorLayer


def point_selection_to_line_layer(point_selection_query: str, layer_name: str) -> QgsVectorLayer:
    sql = "SELECT ST_LineFromMultiPoint(ST_COLLECT(the_geom)) AS line FROM ({}) AS foo".format(point_selection_query)
    uri = get_sql_query_uri(sql, "line")
    return QgsVectorLayer(uri.uri(False), layer_name, "postgres")


def layer_from_database_uri(uri: QgsDataSourceUri, layer_name: str) -> QgsVectorLayer:
    return QgsVectorLayer(uri.uri(False), layer_name, "postgres")


def get_basic_uri() -> QgsDataSourceUri:
    uri = QgsDataSourceUri()
    # set host name, port, database name, username and password
    uri.setConnection("localhost", "5432", "checkins", "user", "password")
    return uri


def get_full_uri(where_clause: str, table: str) -> QgsDataSourceUri:
    uri = get_basic_uri()
    # subset (WHERE clause)
    uri.setDataSource("public", table, "the_geom", where_clause)
    return uri


def get_sql_query_uri(sql: str, geometry_field: str) -> QgsDataSourceUri:
    uri = get_basic_uri()
    uri.setDataSource("", "(" + sql.rstrip(';') + ")", geometry_field, "")
    return uri


def get_pg_connection():
    return psycopg2.connect("dbname=checkins user=user password=password host=localhost port=5432")
