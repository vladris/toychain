import block


# Genesis block with index 0
def make_genesis_block():
    return block.Block(0, None, None)


blockchain = [make_genesis_block()]


# Check if blockchain is valid
def is_valid(blockchain):
    # First block should be genesis block
    if blockchain[0].__dict__ != make_genesis_block().__dict__:
        return False

    # All subsequent blocks should be valid
    for i in range(1, len(blockchain)):
        if not block.is_valid(blockchain[i], blockchain[i - 1]):
            return False

    return True


# Append data to blockchain
def append(data):
    index, prev_hash = blockchain[-1].index + 1, blockchain[-1].hash
    blockchain.append(block.Block(index, data, prev_hash))


# Replace blockchain
def try_replace(new_blockchain):
    global blockchain

    if new_blockchain[-1].index <= blockchain[-1].index:
        print('Provided blockchain shorter than held blockchain')
        return False

    if not is_valid(new_blockchain):
        print('Provided blockchain invalid')
        return False

    blockchain = new_blockchain
    print('Swapped blockchains')
    return True


# Get last block in blockchain
def last():
    return blockchain[-1]
