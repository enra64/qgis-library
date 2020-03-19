from phase1_cdr import cdr_analytics
from qgis_setup.basic import setup_qgis, exit_qgis

qgs = setup_qgis("/home/arne/Documents/git-repos/ubiquitous-systems/basefile.qgz")
cdr_analytics.execute("1324")
exit_qgis("/home/arne/Documents/git-repos/ubiquitous-systems/generated/CDR.qgz", qgs)
