from peewee import *
import psycopg2

conn = psycopg2.connect(host='localhost', user='postgres', password='postgres')
conn.cursor().execute('CREATE DATABASE mydatabase')
conn.close()

db = PostgresqlDatabase('mydatabase', host='localhost', port=5432, user='postgres', password='postgres')

class Ads(Model):
    image = TextField(max_length=255)
    title = TextField(max_length=255)
    location = TextField(max_length=255)
    date = TextField()
    bedrooms = TextField(max_length=255)
    description = TextField(max_length=255)
    price = TextField(max_length=255)
    currency = TextField(max_length=255)

    class Meta:
        database = db
        db_table = 'Ads'

db.connect()
db.create_tables([Ads])
db.close