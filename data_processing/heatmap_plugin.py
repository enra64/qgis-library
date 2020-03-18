from qgis.core import QgsVectorLayer, QgsRasterLayer

from layer_stuff.basic import read_raster_layer


def create_heatmap(input_layer: QgsVectorLayer, persistence_folder: str) -> QgsRasterLayer:
    from processing.core.Processing import Processing
    Processing.initialize()
    import processing

    out_path = "{}/{}-heatmap.tif".format(persistence_folder, input_layer.name())

    processing.run("qgis:heatmapkerneldensityestimation", {'INPUT': input_layer,
                                                           "KERNEL": 4,
                                                           "RADIUS": 0.02,
                                                           # "RADIUS_FIELD": "longitude"
                                                           # "WEIGHT_FIELD": "latitude",
                                                           "PIXEL_SIZE": 0.02,
                                                           "OUTPUT_VALUE": 0,
                                                           "OUTPUT": out_path})

    heatmap_layer_name = "Heatmap from {}".format(input_layer)
    return read_raster_layer(out_path, heatmap_layer_name)
