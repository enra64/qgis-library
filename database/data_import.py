import psycopg2
from qgis.core import QgsDataSourceUri


def get_line_layer():
    "SELECT ST_LineFromMultiPoint(ST_COLLECT(point)) FROM (SELECT point FROM checkins WHERE user_id = '170604' ORDER BY timestamp) AS foo"

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

def get_pg_connection():
    return psycopg2.connect("dbname=checkins user=user password=password")