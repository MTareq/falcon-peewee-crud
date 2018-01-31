import falcon
from .models import init_db
from .resources import RestaurantResource, RestaurantCollection


def create():
    init_db()
    api = falcon.API()
    restuaurnat = RestaurantResource()
    restuaurnat_collection = RestaurantCollection()
    api.add_route('/restaurants/{obj_id}', restuaurnat)
    api.add_route('/restaurants', restuaurnat_collection)
    return api


api = create()
