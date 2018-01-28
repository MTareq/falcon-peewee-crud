import falcon
from .resources import RestaurantResource, RestaurantCollection

app = falcon.API()

restuaurnat = RestaurantResource()
restuaurnat_collection = RestaurantCollection()

app.add_route('/restaurants/{obj_id}', restuaurnat)
app.add_route('/restaurants', restuaurnat_collection)
