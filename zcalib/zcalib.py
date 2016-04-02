import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import registry
from zope.component import getUtility
from interfaces import IModel, IView, IController, IApplication
from helpers import view_model

def main():
    application = getUtility(IApplication, name="application")
    maincontroller = view_model(application)
    maincontroller.run()
    Gtk.main()

if __name__ == '__main__':
    registry.initialize()
    try:
        main()
    except KeyboardInterrupt:
        import sys
        sys.exit(1)
    quit()
