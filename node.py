import block
import blockchain
from bottle import request, route, run
import json
import requests
import sys


# Set of peer nodes
peers = set()


# Decode block from JSON
def decode_block(as_dict):
    return block.Block(
        as_dict['index'], as_dict['data'], as_dict['prev_hash'], as_dict['hash'])


# Get blockchain
@route('/blocks', method='GET')
def get_blocks():
    return json.dumps(
        blockchain.blockchain,
        default=lambda block: block.__dict__)


# Get last block
@route('/block', method='GET')
def get_block():
    return json.dumps(blockchain.last().__dict__)


# Post last block
@route('/block', method='POST')
def post_block():
    body = request.body.read().decode('utf-8')

    # Deserialize block
    new_block = json.loads(body, object_hook = decode_block)

    if new_block.index <= blockchain.last().index:
        print('Held blockchain is longer, ignoring received block')
        return

    if new_block.prev_hash == blockchain.last().hash:
        print('New block can be directly appended')
        blockchain.blockchain.append(new_block)
        broadcast_last()
        return

    # Sync with peers
    sync()


@route('/sync', method='POST')
def sync():
    # Request blockchain from peers
    for response in broadcast(requests.get, '/blocks'):
        chain = json.loads(response.text, object_hook = decode_block)
        if blockchain.try_replace(chain):
            broadcast_last()


# Append block to blockchain
@route('/append', method='POST')
def append():
    blockchain.append(request.body.read().decode('utf-8'))
    broadcast_last()


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


# Broadcast message to all peers
def broadcast(func, path, body=None):
    for peer in peers:
        try:
            yield func(peer + path, body)
        except:
            print(f'Failed to reach {peer}')


# Broadcast last block to all peers
def broadcast_last():
    for _ in broadcast(requests.post, '/block',
        json.dumps(blockchain.last().__dict__)): pass


run(server='waitress', host='localhost', port=int(sys.argv[1]) if len(sys.argv) > 1 else 8080)
