from zope.interface import Interface
from zope.interface import Attribute

class IModel(Interface):
    pass

class IBook(IModel):

    barcode = Attribute("Barcode")
    author = Attribute("Author of book")
    title = Attribute("Title of book")


class IMember(IModel):

    number = Attribute("ID number")
    name = Attribute("Name of member")


class ICirculation(IModel):

    book = Attribute("A book")
    member = Attribute("A member")


class IApplication(IModel):

    """A marker interface"""

class IRelationalDatabase(Interface):

    def commit():
        pass

    def rollback():
        pass

    def cursor():
        pass

    def get_next_id():
        pass


class IObjectDatabase(Interface):

    def commit():
        pass

    def rollback():
        pass

    def container():
        pass

    def get_next_id():
        pass


class IDbOperation(Interface):

    def get():
        pass

    def add():
        pass

    def update():
        pass

    def delete():
        pass

class IView(Interface):
    pass
    # FIXME add methods

class IController(Interface):

    model = Attribute("A Model")
    view = Attribute("A View")
