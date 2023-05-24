import hashlib
import time
import json
import pprint
MINER_PAY = 1
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Crea el bloque génesis
        self.chain.append({
                'index': 1,
                'timestamp': time.time(),
                'transactions': ['Genesis'],
                'proof': 100,
                'previous_hash': '0'*32,
                'hash': hashlib.sha256().hexdigest()
            })
    def new_block(self, previous_hash=None):
        proof = self.chain[-1]['proof']
        dif42 = 1
        miner_pay = 0
        new_hash = None
        new_pow = 100
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof':  new_pow,
            'previous_hash': self.chain[-1]['hash'],
            'hash': new_hash
        }
        new_pow = self.proof_of_work(proof, new_pow, dif42, block['index'])
        self.validate1 = self.proof_of_work(self.chain[-1]['proof'], new_pow, dif42, block['index'])
        self.validate2 = self.proof_of_work2(self.chain[-1]['proof'], new_pow, dif42, block['index'])
        self.hash1 = self.chain[-1]['hash']
        self.hash2 = block['previous_hash']
        self.current_transactions = []
        if self.mine() == 2:
            new_hash = self.hash(block)
            block['hash'] = new_hash
            block['proof'] = new_pow
            self.chain.append(block)
            miner_pay += MINER_PAY
        return block
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.current_transactions[-1]
    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    def  proof_of_work(self, previous_proof, proof, dif42, block):
        if block % 2 == 0:
            dif42 = block
        while not self.valid_proof(previous_proof, proof, dif42):
            proof += 1
        return proof
    def valid_proof(self, previous_proof, proof, dif42):
        prueba  = f'{previous_proof}{proof}'.encode()
        hash_prueba = hashlib.sha256(prueba).hexdigest()
        pat42 = '0'*dif42+'42'
        lng42 = len(pat42)
        return hash_prueba[-lng42:] == pat42
    def proof_of_work2(self, previous_proof, proof, dif42, block):
        if block % 2 == 0:
            dif42 = block
        while not self.second_valid_proof(previous_proof, proof, dif42):
            proof += 1
        return proof
    def second_valid_proof(self, previous_proof, proof, dif42):
        prueba  = f'{previous_proof}{proof}'.encode()
        hash_prueba = hashlib.sha256(prueba).hexdigest()
        pat42 = '0'*dif42+'42'
        lng42 = len(pat42)
        return hash_prueba[-lng42:] == pat42
    def mine(self):
        count = 0
        if self.hash1 == self.hash2:
            count += 1
        if self.validate1 == self.validate2:
            count += 1
        return count
if __name__ == '__main__':
    prueba =  Blockchain()
    prueba.new_transaction('juan', 'pepe', 30)
    prueba.new_transaction('jose', 'manuel', 3999)
    prueba.new_block()
    prueba.new_transaction('manuel', 'sergio', 220293)
    prueba.new_transaction('isabel', 'yolanda',23221)
    prueba.new_block()
    prueba.new_block()
    for blk in prueba.chain:
        pprint.pprint(blk)