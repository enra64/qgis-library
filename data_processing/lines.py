from typing import Dict, List

from qgis.core import QgsGeometry, QgsPoint, QgsVectorLayer, QgsFeature


def create_line_geometry(csv_rows: List[Dict]) -> QgsGeometry:
    points = [QgsPoint(float(row["longitude"]), float(row["latitude"])) for row in csv_rows]
    # noinspection PyCallByClass,PyArgumentList
    return QgsGeometry.fromPolyline(polyline=points)


def create_line_geometry_postgis(linestring_ewkt: str) -> QgsGeometry:
    # noinspection PyCallByClass,PyArgumentList
    return QgsGeometry.fromWkt(linestring_ewkt)


def create_line_layer(geometry: QgsGeometry, name: str) -> QgsVectorLayer:
    result_layer = QgsVectorLayer("LineString?crs=EPSG:4326", name, "memory")
    data_provider = result_layer.dataProvider()
    result_layer.startEditing()
    feature = QgsFeature(result_layer.fields())
    feature.initAttributes(len(result_layer.fields()))
    feature.setGeometry(geometry)
    data_provider.addFeatures([feature])
    result_layer.commitChanges()
    return result_layer
