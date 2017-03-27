import json
import os
import peewee
from peewee import MySQLDatabase

database = host = user = password = ""
dirName = "Joulie"

if ('MYSQL_DATABASE' in os.environ and
    'MYSQL_HOST' in os.environ and
    'MYSQL_USER' in os.environ and
    'MYSQL_PASSWORD' in os.environ):

    database = os.environ.get('MYSQL_DATABASE')
    host = os.environ.get('MYSQL_HOST')
    user = os.environ.get('MYSQL_USER')
    password = os.environ.get('MYSQL_PASSWORD')
else:
    workDir = os.path.dirname(os.path.realpath(__file__))
    index = workDir.rfind(dirName)
    if index == -1:
        raise Exception("Unknown workng directory: " + workDir)

    workDir = workDir[:index + len(dirName)]

    with open(os.path.join(workDir, 'connection.json')) as data_file:
        data = json.load(data_file)

        database = data["database"]
        host = data["host"]
        user = data["user"]
        password = data["password"]

db = MySQLDatabase(database=database, host=host, user=user, passwd=password)


# Base class for the database
class DatabaseModel(peewee.Model):
    class Meta:
        database = db


def database():
    return db
