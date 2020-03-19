from qgis.core import QgsVectorLayer, QgsRasterLayer

from layer_stuff.basic import read_raster_layer


def create_heatmap(input_layer: QgsVectorLayer, persistence_folder: str, name: str) -> QgsRasterLayer:
    from processing.core.Processing import Processing
    Processing.initialize()
    import processing

    out_path = "{}/{}-heatmap.tif".format(persistence_folder, name.replace(" ", "_"))

    processing.run("qgis:heatmapkerneldensityestimation", {'INPUT': input_layer,
                                                           "KERNEL": 4,
                                                           "RADIUS": 0.02,
                                                           "RADIUS_FIELD": "",
                                                           "WEIGHT_FIELD": "",
                                                           "PIXEL_SIZE": 7e-05,
                                                           "OUTPUT_VALUE": 0,
                                                           "OUTPUT": out_path})

    return read_raster_layer(out_path, name)
