Toy blockchain implementation based on [Naivechain](https://github.com/lhartikk/naivechain).

Unlike Naivechain, we don't use websockets, rather everything is handled over
HTTP. Otherwise logic should be very similar. 

Requires `bottle`, `requests`, and `waitress`:

```
pip install bottle requests waitress
```

`bottle` for the node implementation, `requests` to make P2P calls, `waitress`
to play with it locally (default bottle server is single-threaded so sync
requests can't be properly handled).

# block.py

Contains a block consisting of index, data payload, hash of previous node and
hash.

# blockchain.py

Contains the blockchain implementation, genesis block, and functions to append
data (by generating a new block) and to replace blockchain if a longer
blockchain is provided.

# node.py

Webserver with following REST API:

## Peer management

```
/peers [GET]    - retrieve list of peers
/peers [POST]   - add peer (URL as text/plain body)
/peers [DELETE] - delete peer (URL as text/plain body)
```

TODO: sync peers across nodes automatically

## Data APIs

```
/append [POST]  - add data to blockchain (data as text/plain body)
/block [GET]    - returns last block in blockchain as JSON
/blocks [GET]   - returns blockchain as JSON
```

## P2P sync

```
/block [POST]   - attempt to append block to blockchain (block as text/json body)
/sync  [POST]   - force sync with peers
```

# Running

A node can be launched from command line with port as argument. It will run on
`localhost` listening on the given port. For example we can start two nodes with

```
node.py 8080
node.py 8081
```

Peers needs to be connected manually on each node using the `/peers` API as
described above.

Data is added via the `/append` command. After the new block is added to the
node-local blockchain, the node broadcasts it to all known peers by POSTing it
to `<peer>/block`.

When a `/block` POST request arrives, if the index of the block is not greater
than then index of the last block in the blockchain held by the node, the
incoming block is discarded. Otherwise, if the `prev_hash` of the incoming block
is the same as the hash of the last block in the blockchain held by the node,
the incoming block is appended and it is further broadcasted to all known peers
by POSTing it to `<peer>/block`. Otherwise node cannot directly reconcile
incoming block so it triggers a sync as if `/sync` were called.

A `sync` request causes the node to request the full chain from all peers. Each
response is deserialized and an attempt is made to replace the blockchain held
by the node with the blockchain retrieved from a peer. Replacement happens if
the retrieved blockchain is both longer and valid. If held blockchain gets
replaced, last block is broadcasted to all known peers by POSTing it to
`<peer>/block`.
