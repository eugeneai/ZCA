import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

"""Module with implementation helper classes.
"""
from interfaces import IView, IController
from zope.interface import implementer
from zope.component import getAdapter, getMultiAdapter

UI_DIR='glade'

def abs_filename(filename):
    curdir=os.path.abspath(os.path.dirname(__file__))
    xml = os.path.join(curdir, UI_DIR, filename)
    return xml

class UIHelper(object):
    """The UIHelper class used to create
    self.ui field of controllers referencing
    ui widgets of the View.
    """

@implementer(IView)
class View(object):
    """A View."""
    def __init__(self, model = None):
        self.model = model
        self.ui=UIHelper()

class DesignedView(View):
    """A View that is loaded by Gtk Builder."""
    objects=None
    filename=None
    extention=".ui"
    def __init__(self, model = None, filename=None, objects=None):
        super(DesignedView,self).__init__(model=model)
        builder=Gtk.Builder()
        if filename == None:
            filename = self.__class__.filename
        if filename == None:
            filename = self.__class__.__name__.lower()+ \
                self.__class__.extention
        builder.add_from_file(abs_filename(filename))
        self.builder=builder
        self.ui.objects=[]
        if objects == None:
            objects = self.__class__.objects
        if objects == None:
            raise ValueError("no object names supplied")
        for object_name in objects:
            obj=builder.get_object(object_name)
            if obj == None:
                raise KeyError("could not find obect named '{}'".format(object_name))
            self.ui.objects.append(obj)
            setattr(self.ui, object_name, obj)

@implementer(IController)
class Controller(object):
    def __init__(self, model, view):
        self.model=model
        self.view=view
        self.ui=self.view.ui
        self.main_widget=self.view.ui.objects[0] # Hopefully
        view.builder.connect_signals(self)
        self.main_widget.connect('delete_event', self.on_delete_event)
        # self.show_all()

    def initialize(self):
        pass

    def show_all(self):
        self.initialize()
        self.main_widget.show_all()

    def show(self):
        self.show_all()

    def run(self):
        self.main_widget.set_modal(True)
        self.show()

    def hide(self):
        self.main_widget.hide()

    def on_delete_event(self, *args):
        if self.model == None:
            self.hide() # The single-window mode, when self.model==None
        else:
            self.main_widget.destroy()
        return True

    def get_selection(self, selection, column=0):
        _,rows=selection.get_selected_rows()
        view=selection.get_tree_view()
        model=view.get_model()
        for row in rows:
            iter=model.get_iter(row)
            yield model.get_value(iter,column)


def view_model(model, name=''):
    view = getAdapter(model,IView, name=name) # For simplicity suppose the same names for Views and Controllers
    controller = getMultiAdapter((model, view), IController, name=name)
    return controller
