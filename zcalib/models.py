from zope.interface import implementer

from interfaces import IBook
from interfaces import IMember
from interfaces import ICirculation
from interfaces import IApplication

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

@implementer(IApplication)
class Application(object):
    pass
