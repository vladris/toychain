import block


blockchain = [block.make_genesis_block()]


# Validate blockchain
def validate(blockchain):
    # First block should be genesis block
    if blockchain[0] != block.make_genesis_block():
        return False

    # All subsequent blocks should be valid
    for i in range(1, len(blockchain)):
        if not block.validate(blockchain[i], blockchain[i - 1]):
            return False

    return True


# Append data to blockchain
def append(data):
    index, prev_hash = blockchain[-1].index + 1, blockchain[-1].hash
    blockchain.append(block.Block(index, data, prev_hash))


append("Foo")
print(validate(blockchain))
