import time
import json
import hashlib
import requests
from urllib.parse import urlparse

class Blockchain(object):
    """
    This class is responsible for managing the blockchain (surprise)! It will store transactions and have some helper
    methods for adding new blocks to the chain
    """
    def __init__(self):
        self.chain = []
        self.transaction_list = []
        self.nodes = set()

        # genesis block serves as truth anchor the blockchain
        self.create_block(100, 1)

    def register_node(self, address):
        """
        Create a new node for the network
        :param address: <str> IP address of the node
        :return None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def validate_chain(self, chain):
        """
        Determine if the given blockchain is valid or not
        :param chain: <list> blockchain
        :return: <bool> True if valid, False if not
        """
        last_block = chain[0]
        current_index = 1

        # iterate through the chain and validate
        while current_index < len(chain):
            block = chain[current_index]

            if block['hash_of_previous'] != self.hash(last_block):
                return False

            if not self.validate_pow(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index = current_index + 1

        return True

    def reach_consensus(self):
        """
        Consensus Algorithm - based on Nakamoto Consensus
        Replace our chain with the longest one in the network
        :return: True if our chain was replaced, False if it was already the longest one
        """
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        # find the longest chain in the network
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.validate_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain is not None:
            self.chain = new_chain
            return True

        return False

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
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha3_512(block_string).hexdigest()

    @property
    def get_last_block(self):
        return self.chain[-1]


# instantiate the Valerium blockchain
blockchain = Blockchain()

import src.flask.routes as flask

if __name__ == '__main__':
    flask.app.run(host='0.0.0.0', port=9000)
