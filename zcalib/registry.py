import sys
from zope.component import getGlobalSiteManager
from zope.configuration.xmlconfig import xmlconfig

from interfaces import IMember
from interfaces import IBook
from interfaces import ICirculation
from interfaces import IDbOperation

def check_use_relational_db():
    use_rdb = False
    try:
        arg = sys.argv[1]
        if arg == '-r':
            return True
    except IndexError:
        pass
    return use_rdb

def initialize():
    use_rdb = check_use_relational_db()
    if use_rdb:
        xml="rdbconfig.zcml"
    else:
        xml="odbconfig.zcml"
    print ("Using config: {}.".format(xml))
    xmlconfig(open(xml))
