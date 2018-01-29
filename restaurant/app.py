import falcon
from .resources import RestaurantResource, RestaurantCollection


def create():
    api = falcon.API()
    restuaurnat = RestaurantResource()
    restuaurnat_collection = RestaurantCollection()
    api.add_route('/restaurants/{obj_id}', restuaurnat)
    api.add_route('/restaurants', restuaurnat_collection)
    return api


api = create()
