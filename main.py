from qgis._core import QgsProject

from phase1_cdr.cdr import analytics
from qgis_setup.basic import setup_qgis

qgs = setup_qgis("/home/arne/Documents/git-repos/ubiquitous-systems/basefile.qgz")

analytics.execute("24490292", "2007-05-02")

outfile = "/home/arne/Documents/git-repos/ubiquitous-systems/generated/CDR.qgz"
QgsProject.instance().write(outfile)
# qgs.exitQgis()