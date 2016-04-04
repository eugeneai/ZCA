import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from zope.component import getAdapter, getUtility

from models import Member
from models import Book
from models import Circulation
from interfaces import *

from helpers import DesignedView, Controller, view_model

class CirculationWindow(DesignedView):
    objects=[
        'circulation_dialog',
        'issue_member',
        'issue_book',
        'a_apply',
        'catalog_view',
        'member_view',
        'catalog_selection',
        'member_selection'
    ]

class CirculationWindowController(Controller):

    def initialize(self):
        self.initialize_lists()
        self.check_selection()

    def initialize_lists(self):
        cm=Gtk.ListStore(object, str, str, str)
        self.ui.catalog_model=cm
        self.ui.catalog_view.set_model(cm)

        cm.append((Book(), "J.R.R.Tolkien", "Brotherhood of the ring", "123-54654"))
        cm.append((Book(), "J.R.R.Tolkien", "Brotherhood of the ring", "123-54654"))
        cm.append((Book(), "J.R.R.Tolkien", "Brotherhood of the ring", "123-54654"))

        mm=Gtk.ListStore(object, int, str)
        self.ui.member_model=mm
        self.ui.member_view.set_model(mm)
        mm.append((Member(), 123, "Jim Carry"))
        mm.append((Member(), 124, "Ann Carry"))
        mm.append((Member(), 125, "Jim Fox"))

    def on_issue_button_clicked(self, *args):
        member_number = self.ui.issue_member.get_text()
        book_barcode = self.ui.issue_book.get_text()
        self.book_issue(member_number, book_barcode)

    def book_issue(self, member_number, book_barcode):
        member = Member()
        member.number = member_number
        memberdboperation = getAdapter(member, IDbOperation)
        member = memberdboperation.get()[0]

        book = Book()
        book.number = book_barcode
        bookdboperation = getAdapter(book, IDbOperation)
        book = bookdboperation.get()[0]

        circulation = Circulation()
        circulation.member = member
        circulation.book = book
        circulationdboperation = getAdapter(circulation, IDbOperation)
        circulationdboperation.add()

    def on_return_activate(self, *args):
        book_barcode = self.ui.return_book.get_text()
        self.book_return(book_barcode)

    def book_return(self, book_barcode):
        book = Book()
        book.number = book_barcode
        bookdboperation = getAdapter(book, IDbOperation)
        book = bookdboperation.get()[0]

        circulation = Circulation()
        circulation.book = book
        circulationdboperation = getAdapter(circulation, IDbOperation)
        circulationdboperation.delete()

    def on_close_activate(self, *args):
        self.on_delete_event()

    def on_apply_activate(self, *args):
        self.on_delete_event()

    def on_member_selection_changed(self, *args):
        self.check_selection()

    def on_catalog_selection_changed(self, *args):
        self.check_selection()

    def check_selection(self):
        cs=self.ui.catalog_selection.get_selected_rows()
        ms=self.ui.member_selection.get_selected_rows()
        print (cs)
        self.ui.a_apply.set_sensitive(cs and ms)

class MemberWindow(DesignedView):
    objects=[
        'memberwindow',
        'number',
        'name',
        'treeview',
        #'list_store'
    ]

    def initialize(self):
        pass

    def populate_list_store(self):
        self.ui.list_store.clear()
        member = Member()
        memberdboperation = getAdapter(member, IDbOperation)
        members = memberdboperation.get()
        for member in members:
            number = member.number
            name = member.name
            self.ui.list_store.append((member, number, name,))

    def initialize_list(self):
        #FIXME DELETE AFTER DESING IN GLADE
        tvcolumn = gtk.TreeViewColumn('Member Number')
        self.treeview.append_column(tvcolumn)

        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 1)

        tvcolumn = gtk.TreeViewColumn('Member Name')
        self.treeview.append_column(tvcolumn)

        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 2)

class MemberWindowController(Controller):

    def on_add_clicked(self, *args):
        number = self.ui.number.get_text()
        name = self.ui.name.get_text()
        member = Member()
        member.number = number
        member.name = name
        self.add(member)
        self.ui.list_store.append((member, number, name,))

    def add(self, member):
        memberdboperation = getAdapter(member, IDbOperation)
        memberdboperation.add()

    def on_update_clicked(self, *args):
        number = self.ui.number.get_text()
        name = self.ui.name.get_text()
        treeselection = self.ui.treeview.get_selection()
        model, iter = treeselection.get_selected()
        if not iter:
            return
        member = self.ui.list_store.get_value(iter, 0)
        member.number = number
        member.name = name
        self.update(member)
        self.ui.list_store.set(iter, 1, number, 2, name)

    def update(self, member):
        memberdboperation = getAdapter(member, IDbOperation)
        memberdboperation.update()

    def on_delete_clicked(self, *args):
        treeselection = self.ui.treeview.get_selection()
        model, iter = treeselection.get_selected()
        if not iter:
            return
        member = self.ui.list_store.get_value(iter, 0)
        self.delete(member)
        self.ui.list_store.remove(iter)

    def delete(self, member):
        memberdboperation = getAdapter(member, IDbOperation)
        memberdboperation.delete()

    def on_close_clicked(self, *args):
        self.on_delete_event()

class CatalogWindow(DesignedView):
    objects=[
        'catalogwindow',
        'barcode',
        'author',
        'title',
        'treeview'
        ]

    def initialize(self):
        self.populate_list_store()

    def populate_list_store(self):
        self.list_store.clear()
        book = Book()
        bookdboperation = getAdapter(book, IDbOperation)
        books = bookdboperation.get()
        for book in books:
            barcode = book.barcode
            author = book.author
            title = book.title
            self.list_store.append((book, barcode, author, title))

    def initialize_list(self):
        # FIXME REMOVE
        self.list_store = gtk.ListStore(object, str, str, str)
        self.treeview.set_model(self.list_store)

        tvcolumn = gtk.TreeViewColumn('Barcode')
        self.treeview.append_column(tvcolumn)

        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 1)

        tvcolumn = gtk.TreeViewColumn('Author')
        self.treeview.append_column(tvcolumn)

        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 2)

        tvcolumn = gtk.TreeViewColumn('Title')
        self.treeview.append_column(tvcolumn)

        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 3)


class CatalogWindowController(Controller):

    def on_add_clicked(self, *args):
        barcode = self.ui.barcode.get_text()
        author = self.ui.author.get_text()
        title = self.ui.title.get_text()
        book = Book()
        book.barcode = barcode
        book.author = author
        book.title = title
        self.add(book)
        self.ui.list_store.append((book, barcode, author, title))

    def add(self, book):
        bookdboperation = getAdapter(book, IDbOperation)
        bookdboperation.add()

    def on_update_clicked(self, *args):
        barcode = self.ui.barcode.get_text()
        author = self.ui.author.get_text()
        title = self.ui.title.get_text()
        treeselection = self.ui.treeview.get_selection()
        model, iter = treeselection.get_selected()
        if not iter:
            return
        book = self.ui.list_store.get_value(iter, 0)
        book.barcode = barcode
        book.author = author
        book.title = title
        self.update(book)
        self.ui.list_store.set(iter, 1, barcode, 2, author, 3, title)

    def update(self, book):
        bookdboperation = getAdapter(book, IDbOperation)
        bookdboperation.update()

    def on_delete_clicked(self, *args):
        treeselection = self.ui.treeview.get_selection()
        model, iter = treeselection.get_selected()
        if not iter:
            return
        book = self.ui.list_store.get_value(iter, 0)
        self.delete(book)
        self.list_store.remove(iter)

    def delete(self, book):
        bookdboperation = getAdapter(book, IDbOperation)
        bookdboperation.delete()

class MainWindow(DesignedView):
    objects = [
        'mainwindow',
        'circulations',
        'circulations_view',
        ]

class MainWindowController(Controller):

    def on_delete_event(self, *args):
        Gtk.main_quit()

    def on_circulations_activate(self, *args):
        return view_model(self.model.circulations, "circulations").run()

    def on_members_activate(self, *args):
        view_model(self.model.members, "members").show()

    def on_catalog_activate(self, *args):
        view_model(self.model.catalog, "catalog").show()

    def on_about_activate(self, *args):
        pass

    def on_quit_activate(self, *args):
        self.on_delete_event()

    def on_add_clicked(self, *args):
        self.on_circulations_activate()
        self.ui.circulations.append((Circulation(), 1000, "Nikolas Nepeyvoda", "Programming Basics"))

    def on_delete_clicked(self, *args):
        treeselection = self.ui.circulations_view.get_selection()
        model, iter = treeselection.get_selected()
        if not iter:
            return
        circulation = self.ui.circulations.get_value(iter, 0)
        #self.delete(book)
        self.ui.circulations.remove(iter)

    def run(self):
        self.show()

    def initialize(self):
        self.initialize_list()

    def initialize_list(self):
        cs=Gtk.ListStore(object, int, str, str)
        self.circulations=self.ui.circulations=cs
        self.ui.circulations_view.set_model(cs)
        cs.clear()
        for i in range(100):
            cs.append((Circulation(),i+1,"John Doe","Alice in Wonderland"))

if __name__ == '__main__':
    import zcalib
    zcalib.run()
