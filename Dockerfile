FROM python:3-slim

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "restaurant.app:api", "--reload"]
