import json
import falcon
from .models import Restaurant, RestaurantSchema


class BaseResource:
    """Abstract class for falcon resources
       Has methods for orm interactions, queries,
       serializing and deserializing data for falcon consumption.
    """

    def serialize(self, data):
        """Serializes the peewee objects using its corresponding schema
           to be json encoded.

           Args:
               data: Peewee Object or List of objects depending
                     on the instance schema if many == True or not
           Returns:
               sr_data: serialized data to be encoded
        """
        sr_data = self.schema.dump(data)
        return sr_data

    def deserialize(self, json_input, **kwargs):
        """Desrializes and validates the json_input.

           Args:
               json_input: raw input json.
               many(optional): bool To control over how to deserialize
                               regardless of how the schema is initiated.
           Returns:
               clean_data: valid Python dict that complies to the schema.
               errors: marshmallow object containing erros in json_input.
        """
        many = kwargs.get('many', None)
        if many is None:
            clean_data, errors = self.schema.load(json_input)
        else:
            clean_data, errors = self.schema.load(json_input, many=many)
        return clean_data, errors

    def create_object(self, data):
        """Creates a single object in the corresponding table
           Args:
               data: Deserialized input coressponds to model attribute.
           Returns:
               obj: Newly created peewee object.
        """
        obj = self.model.create(**data)
        return obj

    def get_object(self, obj_id):
        """Rerieve a single record given its id
           Args:
               obj_id: object priamary key(id)
           Returns:
               obj: Record if found or 404 if not found
        """
        try:
            obj = self.model.get(self.model.id == obj_id)
        except (self.model.DoesNotExist, ValueError):
            raise falcon.errors.HTTPNotFound
        return obj

    def get_object_list(self, query=None):
        """Returns a list of object based on the passed query
           or it will select all the rows in the table.
           Args:
               query(optional): Peewee query Expression.
        """
        result = self.model.select()
        if query:
            result = result.where(query)
        return result

    def update_object(self, data, obj_id):
        """Updates an object(row) using its primary key(id)
           Args:
               data: dict with changes {'attr': 'change'}
               obj_id: object priamary key(id)
           returns:
               updated: number of rows updated
        """
        try:
            query = self.model.update(**data).where(self.model.id == obj_id)
            updated = query.execute()
        except KeyError:
            raise falcon.errors.HTTPBadRequest
        return updated

    def delete_object(self, obj_id):
        """Deletes an object(row) using its primary key(id)
           Args:
               obj_id: object priamary key(id)
           returns:
               deleted: number of rows deleted
        """
        try:
            query = self.model.delete().where(self.model.id == obj_id)
            deleted = query.execute()
        except self.model.DoesNotExist:
            raise falcon.errors.HTTPNotFound
        return deleted


class Resource(BaseResource):
    """Single Resource abstract class, inherits from BaseClass
       This uses the Falcon event handlers to manage GET, PUT, DELETE
       POST is not supported here since its a change that affect a Collection.
       Each method expects obj_id to the request uri.
    """

    def on_get(self, req, resp, obj_id):
        "Returns a single record using its id"
        obj = self.get_object(obj_id)
        sr_obj = self.serialize(obj)
        resp.body = json.dumps(sr_obj.data)
        return resp

    def on_put(self, req, resp, obj_id):
        "Returns the number of rows updated 1 is successfull 0 is failed update"
        updated = 0
        put_data = req.media
        sr_data, errors = self.deserialize(put_data)
        if errors:
            resp.body = json.dumps(errors)
        elif sr_data:
            updated = self.update_object(sr_data, obj_id)
            resp.body = json.dumps({"updated_rows": updated})
        else:
            resp.body = json.dumps({"updated_rows": updated})
        return resp

    def on_delete(self, req, resp, obj_id):
        "Returns the number of rows deleted 1 is successfull 0 is failed update"
        deleted = self.delete_object(obj_id)
        resp.body = json.dumps({"deleted_rows": deleted})
        return resp


class Collection(BaseResource):
    """Collection of Resources abstract class, inherits from BaseClass
       PUT and DELETE expects query parameters in the request to function.
       POST Ignores query parameters.
       GET can work with and without query parameters.
       query params support advanced comparrison like gt,gte,lt and lte
       Examples: '/restaurants/?opens_at__lt=08:30:00',
                '/restaurants/?name__startswith=kf'
    """

    def format_query(self, params):
        """Function to return multiple peewee query expressions
           based on query params
           Args:
               params: request query params
           Returns:
               query: compound Peewee query expression
        """

        query = None
        for key, value in params.items():
            try:
                field_name, operator = key.split('__')
            except ValueError:
                field_name, operator = key, None
            sub_query = None
            try:
                field = getattr(self.model, field_name)
                if not operator:
                    sub_query = (field == value)
                elif operator == 'lt':
                    sub_query = (field < value)
                elif operator == 'lte':
                    sub_query = (field <= value)
                elif operator == 'gt':
                    sub_query = (field > value)
                elif operator == 'gte':
                    sub_query = (field >= value)
                elif operator == 'contains':
                    sub_query = (field.contains(value))
                elif operator == 'startswith':
                    sub_query = (field.startswith(value))
            except AttributeError:
                continue
            if query is not None and sub_query:
                query = query & sub_query
            elif query is None and sub_query:
                query = sub_query
        return query

    def on_get(self, req, resp):
        """Returns a list of object based on the query,
           or returns all the records in the table
        """
        obj_list = []
        q_params = req.params
        if q_params:
            query = self.format_query(q_params)
            obj_list = self.get_object_list(query)
        else:
            obj_list = self.get_object_list()
        sr_data = self.serialize(obj_list)
        resp.body = json.dumps(sr_data.data)
        return resp

    def on_post(self, req, resp):
        """This is bulk create by default,
           it returns a list of created objects
        """
        created = []
        post_data = req.media
        clean_data, errors = self.deserialize(post_data)
        if errors:
            resp.body = json.dumps(errors)
            return resp
        elif clean_data:
            for data in clean_data:
                created.append(self.create_object(data))
        sr_list = self.serialize(created).data
        resp.body = json.dumps(sr_list)
        return resp

    def on_put(self, req, resp):
        """ Updates records based on query params,
            returns number of updated rows
        """
        put_data = req.media
        updated = 0
        q_params = req.params
        obj_list = []
        if q_params:
            query = self.format_query(q_params)
            obj_list = self.get_object_list(query)

        if obj_list:
            clean_data, errors = self.deserialize(put_data, many=False)
            if errors:
                resp.body = json.dumps(errors)
                return resp
            elif clean_data:
                for obj in obj_list:
                    updated += self.update_object(clean_data, obj.id)
        resp.body = json.dumps({"updated_rows": updated})
        return resp

    def on_delete(self, req, resp):
        """ Updates records based on query params,
            returns number of updated rows
        """
        deleted = 0
        q_params = req.params
        obj_list = []
        if q_params:
            obj_list = self.model.select()
            query = self.format_query(q_params)
            obj_list = self.get_object_list(query)
        if obj_list:
            for obj in obj_list:
                deleted += self.delete_object(obj.id)
        resp.body = json.dumps({"deleted_rows": deleted})
        return resp


class RestaurantResource(Resource):

    def __init__(self):
        self.model = Restaurant
        self.schema = RestaurantSchema()


class RestaurantCollection(Collection):

    def __init__(self):
        self.model = Restaurant
        self.schema = RestaurantSchema(many=True)
