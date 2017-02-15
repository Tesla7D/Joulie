import peewee
from peewee import *

class Book(peewee.Model):
    author = peewee.CharField()
    title = peewee.TextField()

    class Meta:
        database = MySQLDatabase()

class DatabaseManager(object):

    def __init__(self):

        self.db = MySQLDatabase()

        Book.create_table()

    def CreateBook(self):
        book = Book(author="me", title='Peewee is cool')
        book.save()

    def GetBook(self):
        result = ""

        for book in Book.filter(author="me"):
            result += book.title

        return result

    def AddDevice(self):
        return ""