FROM ubuntu:18.04

RUN apt-get update -y \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip


# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# https://github.com/moby/moby/issues/21650
ENV FLASK_APP app.py
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

#ENTRYPOINT [ "python3" ]

#CMD [ "app.py" ]

EXPOSE 5000/tcp
