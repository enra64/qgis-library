from phase1.poi import analytics
from qgis_setup.basic import setup_qgis

qgs = setup_qgis("/home/arne/Documents/git-repos/ubiquitous-systems/basefile.qgz")

#analytics.execute("24490292", "2007-05-02")  # CDR
analytics.execute("170604", "2012-05-12", "Essen")  # POI

# qgs.exitQgis()