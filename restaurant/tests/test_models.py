import datetime


def test_schema_dump(peewee_obj, schema):
    dump_data = schema.dump(peewee_obj).data
    assert dump_data == {'id': 1,
                         'name': 'test_restaurant',
                         'opens_at': '08:30:00',
                         'closes_at': '00:00:00'}


def test_schema_load(raw_obj_data, schema):
    clean_data, errors = schema.load(raw_obj_data)
    assert clean_data == {'name': 'test_restaurant2',
                          'opens_at': datetime.time(12, 30),
                          'closes_at': datetime.time(3, 0)}


def test_schema_dump_many(peewee_obj_list, schema_many):
    dump_data = schema_many.dump(peewee_obj_list).data
    assert dump_data == [{'id': 1,
                          'name': 'test_restaurant3',
                          'opens_at': '09:30:00',
                          'closes_at': '01:00:00'},
                         {'id': 2,
                          'name': 'test_restaurant4',
                          'opens_at': '08:30:00',
                          'closes_at': '00:00:00'}
                         ]


def test_schema_load_many(raw_obj_list, schema_many):
    clean_data, errors = schema_many.load(raw_obj_list)
    assert clean_data == [{'name': 'test_restaurant5',
                           'opens_at': datetime.time(10, 30),
                           'closes_at': datetime.time(22, 0)},
                          {'name': 'test_restaurant6',
                           'opens_at': datetime.time(00, 00),
                           'closes_at': datetime.time(00, 0)}
                          ]
