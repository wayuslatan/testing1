FROM python:3.7-alpine
WORKDIR /opt

#RUN apt-get update && apt-get install -y python python-pip
RUN pip install flask
RUN pip install elasticsearch
RUN python -m pip install elasticsearch

COPY test-app2.py /opt/
COPY ./templates/test2.html /opt/templates/

ENTRYPOINT FLASK_APP=/opt/test-app2.py flask run --host=0.0.0.0 --port=8080