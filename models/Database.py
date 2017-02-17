import json
import os
from peewee import MySQLDatabase

database = host = user = password = ""


if ('MYSQL_DATABASE' in os.environ and
    'MYSQL_HOST' in os.environ and
    'MYSQL_USER' in os.environ and
    'MYSQL_PASSWORD' in os.environ):

    database = os.environ.get('MYSQL_DATABASE')
    host = os.environ.get('MYSQL_HOST')
    user = os.environ.get('MYSQL_USER')
    password = os.environ.get('MYSQL_PASSWORD')
with open('connection.json') as data_file:
    data = json.load(data_file)

    database = data["database"]
    host = data["host"]
    user = data["user"]
    password = data["password"]

db = MySQLDatabase(database=database, host=host, user=user, passwd=password)


def database():
    return db
