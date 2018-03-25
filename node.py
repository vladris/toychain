import blockchain
from bottle import request, route, run
import json


@route('/blocks', method='GET')
def get_blocks():
    return json.dumps(
        blockchain.blockchain,
        default=lambda block: block.__dict__)


@route('/append', method='POST')
def append():
    blockchain.append(request.body.read().decode('utf-8'))


run(host='localhost', port=8080)
