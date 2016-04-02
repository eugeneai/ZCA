from zope.interface import implementer

from interfaces import IBook
from interfaces import IMember
from interfaces import ICirculation
from interfaces import IApplication
from interfaces import IItemList

@implementer(IBook)
class Book(object):

    barcode = ""
    title = ""
    author = ""

@implementer(IMember)
class Member(object):

    number = ""
    name = ""

@implementer(ICirculation)
class Circulation(object):

    book = Book()
    member = Member()

@implementer(IItemList)
class ItemList(object):
    """Contains items
    """

    def __init__(self):
        self.items=[]
        self.ready=False

@implementer(IApplication)
class Application(object):

    members = ItemList()
    catalog = ItemList()
    circulations = ItemList()
