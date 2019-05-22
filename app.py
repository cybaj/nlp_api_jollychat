from flask import Flask, request
import konlpy
from konlpy.tag import Hannanum
import jpype

app = Flask(__name__)
hannanum = Hannanum()

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
    return 'Success'

if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)

