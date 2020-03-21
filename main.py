from phase1.cdr import analytics as cdr_analytics
from phase1.poi import analytics as poi_analytics
from qgis_setup.basic import setup_qgis

qgs = setup_qgis("/home/arne/Documents/git-repos/ubiquitous-systems/basefile.qgz")

cdr_analytics.execute("24490292", "2007-05-02")
# poi_analytics.execute("170604", "2012-05-12", "Essen")

#qgs.exitQgis()
