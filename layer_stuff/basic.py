import re
from typing import Union, List, Optional

from qgis.core import QgsProject, QgsMapLayer, QgsVectorLayer, QgsRasterLayer

from csv_tools.file import guess_layer_name
from layer_stuff.csv_layer_filtering import create_uri_filter_end


def add_layer_to_project(layer: QgsMapLayer):
    project = QgsProject.instance()
    layer_candidates = project.mapLayersByName(layer.name())
    if len(layer_candidates) > 0:
        project.removeMapLayers(layer_candidates)
    project.addMapLayer(layer)


def create_vector_layer_from_csv(file_uri: str,
                                 layer_name: Optional[str],
                                 qgis_subset_filter: Optional[str] = None) -> QgsVectorLayer:
    uri = file_uri + create_uri_filter_end(qgis_subset_filter)
    #print("created URI {} for {}".format(uri, layer_name))
    layer = QgsVectorLayer(uri, "", "delimitedtext")
    feature_count = str(layer.featureCount())

    if layer_name is None:
        layer_name = guess_layer_name(file_uri)

    layer.setName("{} [{}]".format(layer_name, feature_count))
    return layer


def read_raster_layer(file_uri: str, layer_name: Union[str, None]) -> QgsRasterLayer:
    if layer_name is None:
        layer_name = guess_layer_name(file_uri)

    return QgsRasterLayer(file_uri, layer_name)
