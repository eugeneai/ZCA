import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from zope.component import getAdapter

from models import Member
from models import Book
from models import Circulation
from interfaces import IDbOperation

from helpers import DesignedView, Controller

class CirculationWindow(DesignedView):
    objects=[
        'circulationwindow',
        'issue_member',
        'issue_book',
        'return_book',
    ]

class CirculationWindowController(Controller):

    def on_issue_clicked(self, *args):
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

    def on_return_clicked(self, *args):
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


#circulationwindow = CirculationWindow()

class MemberWindow(DesignedView):
    objects=[
        'memberwindow',
        'number',
        'name',
        'treeview',
        'list_store'
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

# memberwindow = MemberWindow()

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

#catalogwindow = CatalogWindow()

class MainWindow(DesignedView):
    objects = [
        'mainwindow',
        ]

class MainWindowController(Controller):

    def on_delete_event(self, *args):
        Gtk.main_quit()

    def on_circulation_activate(self, *args):
        circulationwindow.show()

    def on_member_activate(self, *args):
        memberwindow.show()

    def on_catalog_activate(self, *args):
        catalogwindow.show()

    def on_about_activate(self, *args):
        pass

    def run(self):
        self.show()
