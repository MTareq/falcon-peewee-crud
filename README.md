## Template For Falcon Peewee CRUD Framework

### Summary
This Was intended as a Technical task for delivery hero as part of there hiring process, i was free to use any of the mainstream frameworks like Django and Flask, but i thought i have fun with the task and make something i have always wanted to do which is not using any of the mainstream frameworks and assemble a tiny frame work from Falcon, Peewee and Marshmallow.
The Whole idea was to leave all the bloat behind. Any way i got Rejected but alas i had fun :D


CRUD api for restaurant model, A restaurant object:
- id: int
- name: string
- opens_at: time
- closes_at: time

### Requirements

- falcon
- peewee
- marshmallow
- gunicorn
- pytest

### Running

#### virtualenv

```shell
virtualenv --python=python3 venv
source {venv dir}/bin/activate
pip install -r requirements.txt
gunicorn restaurant.app:api --reload
```
server root `http://127.0.0.1:8000`

#### docker
```shell
docker build -t dh-task .
docker run -p 8000:8000 dh-task
```
server root `http://localhost:8000`

### API Guide
#### Single Resaource operations
- url `/restaurants/:restaurantID`

- GET show restaurant
- PUT updates restaurant 
- DELETE deletes restaurant


#### Collection of resources operations
- url `/restaurants/`
- query params: `[name, closes_at, opens_at]`
- query modifier:
```
__lte: less than or equal,
__gte: greater than or equal,
__lt: less than,
__gt: greater than,
__contains: checks if the resource field contians the submitted param(works with name)
__startswith: checks if the resource field starts with the submitted param (works with name)
```
- POST creates restaurants(bulk create by default so request body should be a list, with single json doc for single creation)
- GET show all restaurants that match the query params.
- PUT updates restaurants that match the query params.
- DELETE deletes restaurants that match the query params.

### Testing

- run `pytest` in the project root.
