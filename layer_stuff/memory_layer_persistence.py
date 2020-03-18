from qgis.core import QgsVectorLayer, QgsVectorFileWriter

from layer_stuff.basic import create_vector_layer_from_csv


def persistify_vector_layer(persistence_folder: str, layer: QgsVectorLayer) -> QgsVectorLayer:
    out_path = "{}/{}.csv".format(persistence_folder, layer.name())
    QgsVectorFileWriter.writeAsVectorFormat(layer, "out_path", "UTF-8", layer.crs(), "ESRI Shapefile")
    return create_vector_layer_from_csv(out_path, layer.name())
