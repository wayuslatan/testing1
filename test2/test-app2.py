from flask import Flask, render_template, request, make_response, g
from elasticsearch import Elasticsearch
import json
import socket

es=Elasticsearch([{'host':'elasticsearch','port':9200}])
app = Flask(__name__)

hostname = socket.gethostname()

@app.route('/')
def test2():
    RAM = 0
    CPU = 0
    GPU = 0

    if request.method == 'GET':
        es=Elasticsearch([{'host':'elasticsearch','port':9200}])
        res = es.search(index='voting', filter_path=['hits.hits._*'], size=10000)

        for each in res['hits']['hits']:
            print(each)
            if each['_source']['option'] == 'RAM':
                RAM = RAM+1
            if each['_source']['option'] == 'GPU':
                GPU = GPU+1
            if each['_source']['option'] == 'CPU':
                CPU = CPU+1

        resp = make_response(render_template(
            'test2.html',
            RAM=RAM,
            CPU=CPU,
            GPU=GPU,
            hostname=hostname
        ))

        return resp
    return 'error!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)