import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import registry
from zope.component import getUtility, getMultiAdapter
from interfaces import IModel, IView, IController

def main():
    application = getUtility(IModel, name="application")
    mainview = getUtility(IView, name="mainview")
    maincontroller = getMultiAdapter((application, mainview), IController, name="maincontroller")
    maincontroller.run()
    Gtk.main()

if __name__ == '__main__':
    registry.initialize()
    try:
        main()
    except KeyboardInterrupt:
        import sys
        sys.exit(1)
