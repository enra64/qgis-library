import sys

from qgis.core import QgsApplication


def find_processing_lib():
    sys.path.append("/usr/share/qgis/python/plugins/")


def setup_qgis() -> QgsApplication:
    # noinspection PyCallByClass,PyTypeChecker
    QgsApplication.setPrefixPath("/usr", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    return qgs


def exit_qgis(qgs):
    qgs.exitQgis()
