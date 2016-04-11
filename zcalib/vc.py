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
        'member_number',
        'member_name',
        'book_title',
        'book_author',
        'book_barcode',
        'a_apply',
        'catalog_view',
        'member_view',
        'catalog_selection',
        'member_selection',
        'select_button',
        'add_member',
        'delete_member',
        'add_book',
        'delete_book'
    ]

class CirculationWindowController(Controller):

    def initialize(self):
        self.initialize_lists()
        self.check_selection()

    def initialize_lists(self):
        cm=Gtk.ListStore(object, str, str, str)
        self.ui.catalog=cm
        self.ui.catalog_view.set_model(cm)
        for _ in range(3):
            b=Book()
            b.title="Brotherhood of the ring"
            b.author="J.R.R.Tolkien"
            b.barcode="123-1232"
            self.append_book(b)

        mm=Gtk.ListStore(object, int, str)
        self.ui.members=mm
        self.ui.member_view.set_model(mm)
        for _ in range(3):
            m=Member()
            m.name="Jim Carry"
            m.number=123
            self.append_member(m)

    def append_member(self, member):
        m=self.ui.members
        m.append((member, member.number, member.name))

    def append_book(self, book):
        m=self.ui.catalog
        m.append((book, book.author, book.title, book.barcode))

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
        self.response(0)

    def on_apply_activate(self, *args):
        self.response(1)

    def on_member_selection_changed(self, *args):
        self.check_selection()

    def on_catalog_selection_changed(self, *args):
        self.check_selection()

    def check_selection(self):
        cs=list(self.get_selection(self.ui.catalog_selection))
        ms=list(self.get_selection(self.ui.member_selection))

        self.ui.a_apply.set_sensitive(cs and ms)
        self.ui.delete_member.set_sensitive(ms)
        self.ui.delete_book.set_sensitive(cs)

        self.ui.add_member.set_sensitive(self.check_member_data())
        self.ui.add_book.set_sensitive(self.check_book_data())

        self.catalog_selection=cs
        self.member_selection=ms

    def check_book_data(self):
        ui=self.ui
        entries=[ui.book_title, ui.book_author, ui.book_barcode]
        return self.check_entries(entries)

    def check_member_data(self):
        ui=self.ui
        entries=[ui.member_name, ui.member_number]
        return self.check_entries(entries)

    def check_entries(self, entries):
        for w in entries:
            text=w.get_text().strip()
            if not text:
                return False
        return True

    def on_entry_text_changed(self, *args):
        self.check_selection()

    def on_add_book_clicked(self, *args):
        pass
    def on_delete_book_clicked(self, *args):
        pass
    def on_add_member_clicked(self, *args):
        pass
    def on_delete_member_clicked(self, *args):
        pass

    def retval(self):
        return self.member_selection, self.catalog_selection

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
        'circulations_view',
        'delete',
        'about_dialog'
        ]

class MainWindowController(Controller):

    def on_delete_event(self, *args):
        Gtk.main_quit()

    def on_circulations_activate(self, *args):
        m=view_model(self.model.circulations, "circulations")
        resp=m.run()
        if resp>0:
            self.bind_circulations(m.member_selection, m.catalog_selection)

    def bind_circulations(self, members, books):
        for member in members:
            for book in books:
                circ=Circulation()
                circ.book=book
                circ.member=member
                self.append_circulation(circ)

    def append_circulation(self, circ):
        self.ui.circulations.append((circ, circ.member.name, circ.book.title))

    def on_menu_about_activate(self, *args):
        ad=self.ui.about_dialog
        ad.set_modal(True)
        ad.show_all()
        ad.run()
        ad.hide()

    on_menu_about_clicked=on_menu_about_activate

    def on_menu_quit_activate(self, *args):
        self.on_delete_event()

    on_menu_quit_clicked=on_menu_quit_activate

    def on_add_clicked(self, *args):
        self.on_circulations_activate()

    on_menu_add_clicked=on_add_clicked

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
        self.check_selection()

    def initialize_list(self):
        cs=Gtk.ListStore(object, str, str)
        self.circulations=self.ui.circulations=cs
        self.ui.circulations_view.set_model(cs)
        cs.clear()
        for i in range(10):
            cs.append((Circulation(),"John Doe","Alice in Wonderland"))

    def check_selection(self):
        s=self.get_selection(self.ui.circulations)
        self.ui.delete.set_sensitive(s)

if __name__ == '__main__':
    import zcalib
    zcalib.run()
