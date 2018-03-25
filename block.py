import hashlib


# Block contains index, data, hash of previous block and hash of block
class Block:
    def __init__(self, index, data, prev_hash, hash=None):
        self.index, self.data, self.prev_hash = index, data, prev_hash
        self.hash = hash_block(self)

        # hash argument is optional, if provided, just check it matches
        # actual hash
        if hash and hash != self.hash:
            raise Error('Inavlid block hash')


# Block hashing function (SHA265 of index, data, and hash of previous block)
def hash_block(block):
    block_hash = hashlib.sha256()
    for data in [block.index, block.data, block.prev_hash]:
        block_hash.update(str(data).encode('utf-8'))
    return block_hash.hexdigest()


# Check if block is valid given previous block
def is_valid(block, prev_block):
    if block.index != prev_block.index + 1:
        return False
    if block.prev_hash != prev_block.hash:
        return False
    if hash_block(block) != block.hash:
        return False
    return True
