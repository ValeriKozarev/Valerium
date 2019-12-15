import unittest
from src.blockchain import Blockchain


class TestBlockchainMethods(unittest.TestCase):
    """
    All unit-testing for the blockchain class exists here
    """

    def test_node_registration(self):
        blockchain = Blockchain()
        self.assertEqual(len(blockchain.nodes), 0)

        blockchain.register_node("http://127.0.0.1:9000")
        self.assertEqual(len(blockchain.nodes), 1)

    def test_create_transaction(self):
        pass

    def test_create_block(self):
        pass

    def test_consensus(self):
        pass

    def test_hash(self):
        pass

    def test_pow(self):
        pass

    def test_scaling_mining_difficulty(self):
        # this aligns with one of my goals to have difficulty scale, easiest way is to script a test
        pass


if __name__ == '__main__':
    unittest.main()
