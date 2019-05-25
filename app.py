from flask import Flask, request
import konlpy
from konlpy.tag import Hannanum
import jpype
import requests
import json
from itertools import combinations

app = Flask(__name__)
hannanum = Hannanum()
dbapi_URL = "http://localhost:5000/graph/"
headers = {'Content-Type': 'application/json; charset=utf-8'} 

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/noun_extract/<uuid>', methods=['GET', 'POST'])
def noun_extract(uuid):
    jpype.attachThreadToJVM()
    extracted_collection = {}
    content = request.json
    # content = {'sent': '트와이스 그리고 아이오아이 좋아여 tt가 저번에 1위 했었죠?'}
    
    extracted_collection['han'] = hannanum.nouns(content['sent'])
    print(extracted_collection)

    URL_insert_node = dbapi_URL + "insert/node/"
    
    for nodename in extracted_collection['han'] :
        print(
            requests.post(URL_insert_node, headers=headers, data=json.dumps({'name': nodename}))
                    )
    edgesets = list(combinations(extracted_collection['han'], 2))

    URL_insert_edge = dbapi_URL + "insert/edge/"

    for edgeset in edgesets :
        print(
            requests.post(URL_insert_edge, headers=headers, data=json.dumps({'firstNodeName': edgeset[0], 'secondNodeName': edgeset[1]}))
            )

    return 'Success'

if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)

