import peewee
from peewee import *

class Book(peewee.Model):
    author = peewee.CharField()
    title = peewee.TextField()

    class Meta:
        database = MySQLDatabase("heroku_c25c250c1ee9407", host="us-cdbr-iron-east-04.cleardb.net", user="b4f20d2e807ead", passwd="2709d0cd")

class DatabaseManager(object):

    def __init__(self):
        self.host = "us-cdbr-iron-east-04.cleardb.net"
        self.username = "b4f20d2e807ead"
        self.password = "2709d0cd"

        self.db = MySQLDatabase(self.host, user=self.username, passwd=self.password)

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