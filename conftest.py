import datetime
import pytest
from restaurant.models import Restaurant, RestaurantSchema
from peewee import SqliteDatabase
from playhouse.test_utils import test_database


test_db = SqliteDatabase(':memory:')


@pytest.fixture()
def schema():
    return RestaurantSchema()


@pytest.fixture()
def schema_many():
    return RestaurantSchema(many=True)


@pytest.fixture()
def peewee_obj():
    with test_database(test_db, (Restaurant,), create_tables=True):
        data = {'name': 'test_restaurant',
                'opens_at': datetime.time(8, 30),
                'closes_at': datetime.time(0, 0)}
        obj = Restaurant.create(**data)
    return obj


@pytest.fixture()
def raw_obj_data():
    data = {'name': 'test_restaurant2',
            'opens_at': '12:30:00',
            'closes_at': '03:00:00'}
    return data


@pytest.fixture()
def peewee_obj_list():
    obj_list = []
    with test_database(test_db, (Restaurant,), create_tables=True):
        data_list = [{'name': 'test_restaurant3',
                      'opens_at': datetime.time(9, 30),
                      'closes_at': datetime.time(1, 0)},
                     {'name': 'test_restaurant4',
                      'opens_at': datetime.time(8, 30),
                      'closes_at': datetime.time(0, 0)}
                     ]
        for data in data_list:
            obj_list.append(Restaurant.create(**data))
    return obj_list


@pytest.fixture()
def raw_obj_list():
    data_list = [{'name': 'test_restaurant5',
                  'opens_at': '10:30:00',
                  'closes_at': '22:00:00'},
                 {'name': 'test_restaurant6',
                  'opens_at': '00:00:00',
                  'closes_at': '00:00:00'}]
    return data_list
