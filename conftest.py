import datetime
import pytest
import falcon
from falcon import testing
from peewee import SqliteDatabase
from playhouse.test_utils import test_database
from restaurant.models import Restaurant, RestaurantSchema
from restaurant.resources import Resource, Collection


test_db = SqliteDatabase(':memory:')


class TestRestaurant(Restaurant):
    class Meta:
        database = test_db


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
def raw_bulk_data():
    data = [{"opens_at": "01:36:07",
             "name": "Orn-Wilderman",
             "closes_at": "05:07:31"},
            {"opens_at": "08:30:46",
             "name": "Schoen, Hane and Windler",
             "closes_at": "00:01:46"},
            {"opens_at": "05:25:35",
             "name": "Pfeffer and Sons",
             "closes_at": "05:46:38"},
            {"opens_at": "01:16:07",
             "name": "Gutkowski-Gibson",
             "closes_at": "01:42:12"},
            {"opens_at": "10:43:53",
             "name": "Cremin-Upton",
             "closes_at": "01:30:37"}]
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


class TestRestaurantResource(Resource):

    def __init__(self):
        self.model = TestRestaurant
        self.schema = RestaurantSchema()


class TestRestaurantCollection(Collection):

    def __init__(self):
        self.model = TestRestaurant
        self.schema = RestaurantSchema(many=True)


@pytest.fixture(scope="module")
def client():
    test_db.connect()
    test_db.create_table(TestRestaurant)
    api = falcon.API()
    restuaurnat = TestRestaurantResource()
    restuaurnat_collection = TestRestaurantCollection()
    api.add_route('/restaurants/{obj_id}', restuaurnat)
    api.add_route('/restaurants', restuaurnat_collection)
    return testing.TestClient(api)


@pytest.fixture
def restaurants_path():
    path = '/restaurants/'
    return path
