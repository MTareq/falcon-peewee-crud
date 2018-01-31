def test_create_obj(client, raw_obj_data, restaurants_path):
    "Creates 2 single restaurant with 2 post requests"

    expected = {'name': 'test_restaurant2',
                'opens_at': '12:30:00',
                'closes_at': '03:00:00',
                'id': 1}
    body = [raw_obj_data]  # post always expect a list
    post_res = client.simulate_post(restaurants_path, json=body)  # creates 1st restaurant
    assert post_res.status_code == 200
    assert post_res.json[0] == expected
    expected['id'] = 2
    post_res = client.simulate_post(restaurants_path, json=body)  # creates 2nd restaurant
    assert post_res.status_code == 200
    assert post_res.json[0] == expected


def test_bulk_create(client, raw_bulk_data, restaurants_path):
    "Creates 5 restaurants in single request"

    body = raw_bulk_data
    post_res = client.simulate_post(restaurants_path, json=body)  # creates 1st restaurant
    assert post_res.status_code == 200


def test_get_object(client, restaurants_path):
    "Get restaurants with id=1 and id=8 which does not exist"

    expected = {'name': 'test_restaurant2',
                'opens_at': '12:30:00',
                'closes_at': '03:00:00',
                'id': 1}
    get_res = client.simulate_get(restaurants_path + '1')
    assert get_res.json == expected
    get_res = client.simulate_get(restaurants_path + '8')
    assert get_res.status_code == 404


def test_get_list_of_objects(client, restaurants_path):
    "Get all restaurants"

    get_res = client.simulate_get(restaurants_path)
    assert len(get_res.json) == 7  # initial 2 restaurants and another 5 from the bulk create


def test_update_object(client, restaurants_path):
    "Update restaurant with id = 1 name to 'test_restaurant1' from 'test_restaurant2' "

    expected = {'name': 'test_restaurant1',
                'opens_at': '12:30:00',
                'closes_at': '03:00:00',
                'id': 1}
    update = {"name": "test_restaurant1"}
    put_res = client.simulate_put(restaurants_path + '1', json=update)
    assert put_res.json == {"updated_rows": 1}
    get_res = client.simulate_get(restaurants_path + '1')
    assert get_res.json == expected


def test_update_multiple_objects(client, restaurants_path):
    "Increases opens_at & closes_at by 1 hour of all restaurant that names starts with 'test_'"

    expected = {'name': 'test_restaurant1',
                'opens_at': '13:30:00',
                'closes_at': '04:00:00',
                'id': 1}
    update = {"opens_at": '13:30:00', 'closes_at': '04:00:00'}
    params = {"name__startswith": "test_"}
    put_res = client.simulate_put(restaurants_path, json=update, params=params)
    assert put_res.json == {"updated_rows": 2}
    get_res = client.simulate_get(restaurants_path + '1')
    assert get_res.json == expected


def test_delete_object(client, restaurants_path):
    "Deletes the restaurant with id=7"

    delete_res = client.simulate_delete(restaurants_path + '7')
    assert delete_res.json == {"deleted_rows": 1}
    get_res = client.simulate_get(restaurants_path)
    assert len(get_res.json) == 6


def test_delete_multiple_objects(client, restaurants_path):
    "Deletes all restaurants that closes at 5am or earlier"

    params = {"closes_at__lte": "05:00:00"}
    delete_res = client.simulate_delete(restaurants_path, params=params)
    assert delete_res.json == {"deleted_rows": 4}
    get_res = client.simulate_get(restaurants_path)
    assert len(get_res.json) == 2
