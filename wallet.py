import hashlib
import json
from time import time
from flask import Flask, jsonify, request
from uuid import uuid4

class KashmirBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_op = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_op[:4] == '0000':
                return new_proof
            new_proof += 1

    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def add_transaction(self, sender, receiver, amount):
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return self.get_previous_block()['index'] + 1

# Create web app
app = Flask(__name__)
node_address = str(uuid4()).replace('-', '')
blockchain = KashmirBlockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(prev_block['proof'])
    prev_hash = blockchain.hash(prev_block)
    blockchain.add_transaction(sender="Network", receiver=node_address, amount=1)
    block = blockchain.create_block(proof, prev_hash)
    return jsonify({'message': 'Block mined!',
                    'block': block}), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({'chain': blockchain.chain,
                    'length': len(blockchain.chain)}), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json_data = request.get_json()
    required = ['sender', 'receiver', 'amount']
    if not all(k in json_data for k in required):
        return 'Missing values', 400
    index = blockchain.add_transaction(json_data['sender'], json_data['receiver'], json_data['amount'])
    return jsonify({'message': f'Transaction added to block {index}'}), 201

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to KashmirCoin Blockchain API"

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
