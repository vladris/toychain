import blockchain
from bottle import request, route, run
import json


# Set of peer nodes
peers = set()


# Get blockchain
@route('/blocks', method='GET')
def get_blocks():
    return json.dumps(
        blockchain.blockchain,
        default=lambda block: block.__dict__)


# Append block to blockchain
@route('/append', method='POST')
def append():
    blockchain.append(request.body.read().decode('utf-8'))


# Get list of peer nodes
@route('/peers', method='GET')
def list_peers():
    return json.dumps(list(peers))


# Add peer
@route('/peers', method='POST')
def add_peer():
    peers.add(request.body.read().decode('utf-8'))


# Remove peer
@route('/peers', method='DELETE')
def remove_peer():
    peers.remove(request.body.read().decode('utf-8'))


run(host='localhost', port=8080)
