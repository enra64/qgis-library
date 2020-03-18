import re
from typing import Union

from qgis.core import QgsProject, QgsMapLayer, QgsVectorLayer, QgsRasterLayer

from csv_tools.file import guess_layer_name


def add_layer_to_project(layer: QgsMapLayer):
    project = QgsProject.instance()
    layer_candidates = project.mapLayersByName(layer.name())
    if len(layer_candidates) > 0:
        project.removeMapLayers(layer_candidates)
    project.addMapLayer(layer)


def create_vector_layer_from_csv(file_uri: str, layer_name: Union[str, None]) -> QgsVectorLayer:
    layer = QgsVectorLayer(file_uri, "", "delimitedtext")
    feature_count = str(layer.featureCount())

    if layer_name is None:
        layer_name = guess_layer_name(file_uri)

    layer.setName("{} [{}]".format(layer_name, feature_count))
    return layer


def read_raster_layer(file_uri: str, layer_name: Union[str, None]) -> QgsRasterLayer:
    if layer_name is None:
        layer_name = guess_layer_name(file_uri)

    return QgsRasterLayer(file_uri, layer_name)
