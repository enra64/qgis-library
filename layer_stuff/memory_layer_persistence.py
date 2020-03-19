from qgis.core import QgsVectorLayer, QgsVectorFileWriter

from layer_stuff.basic import create_vector_layer_from_csv


def persistify_vector_layer(persistence_folder: str, layer: QgsVectorLayer) -> QgsVectorLayer:
    filename = layer.name().replace(" ", "_")
    out_path = "{}{}.shp".format(persistence_folder, filename)
    QgsVectorFileWriter.writeAsVectorFormat(layer, out_path, "UTF-8", layer.crs(), "ESRI Shapefile")
    return QgsVectorLayer(out_path, layer.name(), "ogr")
