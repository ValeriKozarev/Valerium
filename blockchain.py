import time
import json
import hashlib
from uuid import uuid4
from flask import Flask, jsonify, request


class Blockchain(object):
    """
    This class is responsible for managing the blockchain (surprise)! It will store transactions and have some helper
    methods for adding new blocks to the chain
    """

    # pythonic constructor
    def __init__(self):
        self.chain = []
        self.transaction_list = []

        # genesis block serves as truth anchor the blockchain
        self.create_block(100, 1)

    # creates a new block and adds it to the chain
    def create_block(self, proof, hash_of_previous=None):
        """
        Create a new block
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param hash_of_previous: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transaction_list,
            'proof': proof,
            'hash_of_previous': hash_of_previous or self.hash(self.chain[-1])
        }

        # reset the transaction list for the next block
        self.transaction_list = []

        # append this (now finished) block
        self.chain.append(block)
        return block

    def create_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction that will be stored in the upcoming mined block
        :param sender: <str> address of the sender
        :param recipient: <str> address of the recipient
        :param amount: <int> value of the transaction
        :return: <int> index of the aforementioned upcoming mined block
        """
        self.transaction_list.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.get_last_block['index'] + 1

    def create_pow(self, proof_of_previous):
        """
        Simple Proof-of-Work algorithm:
            1) Given a number p (proof_of_previous) which is the previous proof
            2) Find a number g (the new proof that we are generating) such that hash(pg) leads with 4 zeroes
        :param proof_of_previous: <int>
        :return: <int> proof of work for the new block
        """
        proof = 0
        while self.validate_pow(proof_of_previous, proof) is False:
            proof = proof + 1

        return proof

    @staticmethod
    def validate_pow(last_proof, proof):
        """
        Validate the proof submitted for the block, should be hard to prove and easy to check.
        Criteria: does hash(last_proof, proof) have 4 leading zeroes?
        :param last_proof: <int> proof of last block
        :param proof: <int> proof of work for the new block
        :return: True if criteria is met, False if not
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha3_512(guess).hexdigest()

        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        Hash the given block using SHA-3 (no weak crypto here, Dr. Reaves)
        :param block: <dict> block
        :return: <str> hash of the block
        """
        block_stirng = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha3_512(block_stirng).hexdigest()

    @property
    def get_last_block(self):
        return self.chain[-1]


"""
Flask stuff
"""
# instantiate the Flask node
app = Flask(__name__)

# generate unique address for our node
identifier = str(uuid4()).replace('-', '')

# instantiate the Valerium blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # run proof-of-work algorithn
    last_block = blockchain.get_last_block
    last_proof = last_block["proof"]
    proof = blockchain.create_pow(last_proof)

    # receive reward on successful mine (indicate with sender = "0"
    blockchain.create_transaction("0", identifier, 1)

    # forge the new block
    previous_hash = blockchain.hash(last_block)
    new_block = blockchain.create_block(proof, previous_hash)

    response = {
        "message": "new block has been forged",
        "index": new_block["index"],
        "transactions": new_block["transactions"],
        "proof": new_block["proof"],
        "hash_of_previous": new_block["hash_of_previous"]
    }

    return jsonify(response), 201


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # store the request
    values = request.get_json(force=True)

    # validate the request
    required_fields = ["sender", "recipient", "amount"]
    if not all(k in values for k in required_fields):
        return "Invalid request format", 400

    # create the new transaction
    index = blockchain.create_transaction(values["sender"], values["recipient"], values["amount"])
    response = {"message": f'Transaction will be added to block at index {index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
