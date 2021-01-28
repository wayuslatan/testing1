from flask import Flask, render_template, request, make_response, g
from elasticsearch import Elasticsearch
from datetime import datetime
import os
import socket
import random
import json

print(datetime.now())

es=Elasticsearch([{'host':'elasticsearch1','port':9200}])
app = Flask(__name__)

os.environ['OPTION1'] = 'GPU'
os.environ['OPTION2'] = 'CPU'
os.environ['OPTION3'] = 'RAM'

hostname = socket.gethostname()

@app.route('/', methods=['POST','GET'])
def test1():
	option = None

	if request.method == 'POST':
		es=Elasticsearch([{'host':'elasticsearch1','port':9200}])
		#redis = get_redis()

		option = request.form['option']
		#data = json.dumps({'timestamp': datetime.now(), 'option': option, 'hostname': hostname})
		#revision2
		data = {
			'time': datetime.now(),
			'option': option,
			'hostname': hostname
		}

		#redis.rpush('votes', data)
		es.indices.create(index='voting', ignore=400)
		res=es.index(index='voting',body=data)

	resp = make_response(render_template(
        'test1.html',
        OPTION1=os.getenv('OPTION1'),
        OPTION2=os.getenv('OPTION2'),
		OPTION3=os.getenv('OPTION3'),
		hostname=hostname
    ))

	return resp
	
	#print(hostname)
	#print(os.getenv('OPTION1'))
	#print(os.getenv('OPTION1'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)