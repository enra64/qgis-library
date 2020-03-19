import sys

from qgis.core import QgsApplication, QgsProject


def find_processing_lib():
    sys.path.append("/usr/share/qgis/python/plugins/")


def setup_qgis(project_filename: str) -> QgsApplication:
    # noinspection PyCallByClass,PyTypeChecker
    QgsApplication.setPrefixPath("/usr", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    find_processing_lib()
    QgsProject.instance().read(project_filename)
    return qgs


def exit_qgis(outfile: str, qgs: QgsApplication):
    qgs.exitQgis()
