from typing import Dict, List

from qgis.core import QgsGeometry, QgsPoint, QgsVectorLayer, QgsFeature


def create_line_geometry(csv_rows: List[Dict]) -> QgsGeometry:
    points = [QgsPoint(float(row["longitude"]), float(row["latitude"])) for row in csv_rows]
    return QgsGeometry.fromPolyline(polyline=points)


def create_line_layer(geometry: QgsGeometry, name: str) -> QgsVectorLayer:
    result_layer = QgsVectorLayer("Point", name, "memory")
    data_provider = result_layer.dataProvider()
    result_layer.startEditing()
    feature = QgsFeature(result_layer.fields())
    feature.setGeometry(geometry)
    data_provider.addFeatures([feature])
    result_layer.commitChanges()
    return result_layer
