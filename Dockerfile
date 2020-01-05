FROM python:3.8.1-alpine3.11

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# https://github.com/moby/moby/issues/21650
ENV FLASK_APP app.py
ENV FLASK_ENV=development
# For Python 3.6
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000/tcp
