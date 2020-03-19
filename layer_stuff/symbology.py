from typing import List

from PyQt5.QtGui import QPainter
from qgis.PyQt import QtGui
from qgis.core import QgsVectorLayer, QgsArrowSymbolLayer, QgsFillSymbol, QgsRasterLayer, \
    QgsSingleBandPseudoColorRenderer, QgsColorRampShader, QgsRasterShader, QgsRasterBandStats, QgsRasterDataProvider, \
    QgsRasterRenderer


# noinspection PyCallByClass,PyArgumentList
def set_arrow_symbology(layer: QgsVectorLayer):
    layer_symbol = layer.renderer().symbol()
    arrow_symbol_layer = QgsArrowSymbolLayer.create(
        {'arrow_width': '5', 'head_length': '4', 'head_thickness': '6', 'head_type': '0', "is_curved": "0"}
    )
    arrow_fill_sub_symbol = QgsFillSymbol.createSimple(
        {'color': '#8bcfff', 'outline_color': '#000000', 'outline_style': 'solid', 'outline_width': '1'}
    )
    arrow_symbol_layer.setSubSymbol(arrow_fill_sub_symbol)
    layer_symbol.changeSymbolLayer(0, arrow_symbol_layer)


def __get_color_ramp_items(renderer: QgsRasterRenderer, provider: QgsRasterDataProvider, color: QtGui.QColor) -> List[QgsColorRampShader.ColorRampItem]:
    bands = renderer.usesBands()
    band_statistics = provider.bandStatistics(bands[0], QgsRasterBandStats.All)
    minValue = band_statistics.minimumValue
    maxValue = band_statistics.maximumValue

    min_color = QtGui.QColor(color)
    min_color.setAlpha(0)
    max_color = QtGui.QColor(color)
    max_color.setAlpha(255)

    return [
        QgsColorRampShader.ColorRampItem(minValue, min_color),
        QgsColorRampShader.ColorRampItem(maxValue, max_color),
    ]


def set_color_heatmap_symbology(layer: QgsRasterLayer, color: QtGui.QColor):
    provider = layer.dataProvider()
    renderer = layer.renderer()

    color_ramp_items = __get_color_ramp_items(renderer, provider, color)

    color_ramp = QgsColorRampShader()
    color_ramp.setColorRampItemList(color_ramp_items)
    color_ramp.setColorRampType(QgsColorRampShader.Interpolated)

    raster_shader = QgsRasterShader()
    raster_shader.setRasterShaderFunction(color_ramp)

    renderer = QgsSingleBandPseudoColorRenderer(
        layer.dataProvider(),
        layer.type(),
        raster_shader
    )

    layer.setBlendMode(QPainter.CompositionMode_Multiply)
    layer.setRenderer(renderer)
