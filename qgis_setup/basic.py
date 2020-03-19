import sys

from PyQt5.QtWidgets import QApplication
from qgis.core import QgsApplication, QgsProject


def find_processing_lib():
    sys.path.append("/usr/share/qgis/python/plugins/")


def setup_qgis(project_filename: str) -> QgsApplication:
    #app = QApplication([])
    QgsApplication.setPrefixPath("/usr", True)
    QgsApplication.initQgis()
    qgs = QgsApplication([], False)

    find_processing_lib()
    print(qgs)

    QgsProject.instance().read(project_filename)
    return qgs

