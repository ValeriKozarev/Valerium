import time
import json
import hashlib


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

    def create_pow(self):
        pass

    def validate_pow(self):
        pass

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
