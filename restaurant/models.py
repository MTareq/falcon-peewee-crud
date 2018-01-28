from peewee import SqliteDatabase, Model, CharField, TimeField
from marshmallow import Schema, fields

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

    id = fields.int(dump_only=True)
    name = fields.Str()
    opens_at = fields.Time()
    closes_at = fields.Time()
