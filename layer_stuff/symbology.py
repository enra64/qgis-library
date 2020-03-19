from typing import List, Optional, Union

from PyQt5.QtGui import QPainter
from qgis.PyQt import QtGui
from qgis.core import QgsVectorLayer, QgsArrowSymbolLayer, QgsFillSymbol, QgsRasterLayer, \
    QgsSingleBandPseudoColorRenderer, QgsColorRampShader, QgsRasterShader, QgsRasterBandStats, QgsRasterDataProvider, \
    QgsRasterRenderer, QgsMarkerSymbol, QgsFontMarkerSymbolLayer, QgsPropertyCollection, QgsProperty


# noinspection PyCallByClass,PyArgumentList
def set_arrow_symbology(layer: QgsVectorLayer):
    layer_symbol = layer.renderer().symbol()
    arrow_symbol_layer = QgsArrowSymbolLayer.create(
        {'arrow_width': '3', 'head_length': '4', 'head_thickness': '4', 'head_type': '0', "is_curved": "0"}
    )
    arrow_fill_sub_symbol = QgsFillSymbol.createSimple(
        {'color': '#8bcfff', 'outline_color': '#000000', 'outline_style': 'solid', 'outline_width': '0.5'}
    )
    arrow_symbol_layer.setSubSymbol(arrow_fill_sub_symbol)
    layer_symbol.changeSymbolLayer(0, arrow_symbol_layer)


def set_font_symbology(layer: QgsVectorLayer, text_source_field: str, font_size: int, color: QtGui.QColor):
    # noinspection PyCallByClass, PyArgumentList
    symbol = QgsMarkerSymbol.createSimple(
        {'angle': '0', 'chr': 'A', 'color': '40,142,205,255', 'font': 'Sans Serif', 'horizontal_anchor_point': '1',
         'joinstyle': 'bevel', 'offset': '0,0', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_unit': 'MM',
         'outline_color': '35,35,35,255', 'outline_width': '0', 'outline_width_map_unit_scale': '3x:0,0,0,0,0,0',
         'outline_width_unit': 'MM', 'size': '2', 'size_map_unit_scale': '3x:0,0,0,0,0,0', 'size_unit': 'MM',
         'vertical_anchor_point': '1'}
    )

    font_symbol_layer = QgsFontMarkerSymbolLayer("sans", "C", font_size, color)
    font_property = QgsProperty()
    font_property.setField(text_source_field)
    font_symbol_layer.setDataDefinedProperty(8, font_property)

    symbol.deleteSymbolLayer(0)
    symbol.insertSymbolLayer(0, font_symbol_layer)
    layer.renderer().setSymbol(symbol)


def set_cross_symbol(layer: QgsVectorLayer, desired_symbol: str, color: Union[None, str, QtGui.QColor]):
    """
    :param layer: the layer of which the symbology should be changed
    :param desired_symbol: one of circle, square, cross, rectangle, diamond, pentagon, triangle, equilateral_triangle,
                            star, regular_star, arrow, filled_arrowhead, or x
    :param color: color, or none. can also be a well-known color string, like "red"
    :return:
    """
    if color is None:
        color = "red"
    # noinspection PyCallByClass, PyArgumentList
    symbol = QgsMarkerSymbol.createSimple(
        {'angle': '0', 'color': color, 'horizontal_anchor_point': '1', 'joinstyle': 'bevel', 'name': 'cross',
         'offset': '0,0', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_unit': 'MM',
         'outline_color': '35,35,35,255', 'outline_style': 'solid', 'outline_width': '0',
         'outline_width_map_unit_scale': '3x:0,0,0,0,0,0', 'outline_width_unit': 'MM', 'scale_method': 'diameter',
         'size': '6', 'size_map_unit_scale': '3x:0,0,0,0,0,0', 'size_unit': 'MM', 'vertical_anchor_point': '1'})
    layer.renderer().setSymbol(symbol)


def __get_color_ramp_items(renderer: QgsRasterRenderer, provider: QgsRasterDataProvider, color: QtGui.QColor) -> List[
    QgsColorRampShader.ColorRampItem]:
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
