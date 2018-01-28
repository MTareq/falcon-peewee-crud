from peewee import SqliteDatabase, Model, CharField, TimeField
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
