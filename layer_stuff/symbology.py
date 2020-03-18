from PyQt5.uic.properties import QtGui
from qgis.core import QgsVectorLayer, QgsArrowSymbolLayer, QgsFillSymbol, QgsRasterLayer, \
    QgsSingleBandPseudoColorRenderer, QgsColorRampShader, QgsRasterShader


def set_arrow_symbology(layer: QgsVectorLayer):
    layer_symbol = layer.renderer().symbol()
    arrow_symbol_layer = QgsArrowSymbolLayer.create(
        {'arrow_width': '5', 'head_length': '4', 'head_thickness': '6', 'head_type': '0'})
    arrow_fill_sub_symbol = QgsFillSymbol.createSimple(
        {'color': '#8bcfff', 'outline_color': '#000000', 'outline_style': 'solid', 'outline_width': '1'})
    arrow_symbol_layer.setSubSymbol(arrow_fill_sub_symbol)
    layer_symbol.changeSymbolLayer(0, arrow_symbol_layer)


def set_color_heatmap_symbology(layer: QgsRasterLayer, color: QtGui.QColor):
    provider = layer.dataProvider()
    band_statistics = provider.bandStatistics()
    min = band_statistics.minimumValue
    max = band_statistics.maximumValue

    raster_shader = QgsRasterShader()
    color_ramp = QgsColorRampShader()

    min_color = QtGui.QColor(color)
    min_color.setAlpha(0)
    max_color = QtGui.QColor(color)
    max_color.setAlpha(0)

    color_ramp_items = [
        QgsColorRampShader.ColorRampItem(min, min_color, str(min)),
        QgsColorRampShader.ColorRampItem(max, max_color, str(max)),
    ]

    color_ramp.setColorRampItemList(color_ramp_items)
    color_ramp.setColorRampType(QgsColorRampShader.Interpolated)
    raster_shader.setRasterShaderFunction(color_ramp)

    renderer = QgsSingleBandPseudoColorRenderer(
        layer.dataProvider(),
        1,
        raster_shader
    )

    renderer.setOpacity(0.8)

    layer.setRenderer(renderer)
