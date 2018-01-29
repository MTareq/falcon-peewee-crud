import os
from peewee import SqliteDatabase, Model, CharField, TimeField, OperationalError
from marshmallow import Schema, fields

if os.environ.get('TESTING', None):
    db = SqliteDatabase(':memory:')
    del os.environ['TESTING']
else:
    db = SqliteDatabase('dh-task.db')


class Restaurant(Model):
    """
        Peewee model representing a Restaurant

        Attributes:
            name: string representing Restaurant name.
            opens_at: datetime.time structure
                      representing when the Restaurant opens.
            closes_at: datetime.time structure
                       representing when the Restaurant closes.
    """

    class Meta:
        "Locks this tabel to be written on the specified database"

        database = db

    name = CharField()
    opens_at = TimeField()
    closes_at = TimeField()


class RestaurantSchema(Schema):
    "Marshmallow schema to mirror the Restaurant model"

    id = fields.Int(dump_only=True)
    name = fields.Str()
    opens_at = fields.Time()
    closes_at = fields.Time()


try:
    db.connect()
    db.create_table(Restaurant)
    db.close()
except OperationalError:
    pass
