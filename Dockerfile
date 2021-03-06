FROM python:3.8.1-slim

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

# COPY . /app  should volume the local folder

# https://github.com/moby/moby/issues/21650
ENV FLASK_APP app.py
ENV FLASK_ENV=development
# For Python 3.6
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PG_HOST postgresql
ENV GRAFANA_HOST grafana
ENV PROM_HOST prometheus
ENV PROM_PUSHGATEWAY pushgateway

ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000/tcp
