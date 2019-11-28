# Author: Valeri Kozarev
# Inspired by https://cranklin.wordpress.com/2017/07/11/lets-create-our-own-cryptocurrency/
# Valerium is a non-ICO'd cryptocurrency that is powered by elliptic curve cryptography https://cryptography.io/en/latest/


#/////////////////////////////////////////////////////
# TODO: Refactor this class (uses pyelliptic which has been deprecated)
#/////////////////////////////////////////////////////


# init method
def __init__(self, private_key=None, public_key=None):
    if private_key is not None and public_key is not None:
        self.__private_key__ = private_key.decode('hex')
        self.__public_key__ = public_key.decode('hex')

    self.ecc = self.generate_ecc_instance()
 

# generate the instance for Elliptic Curve Cryptography
def generate_ecc_instance(self):
    if self.__private_key__ is None or self.__public_key__ is None:
        print("ECC keys not provided.  Generating ECC keys")
        ecc = pyelliptic.ECC(curve='secp256k1')
        self.__private_key__ = ecc.get_privkey()
        self.__public_key__ = ecc.get_pubkey()
    else:
        ecc = pyelliptic.ECC(curve='secp256k1', privkey=self.__private_key__, pubkey=self.__public_key__)
    return ecc
 

# get the public key of the wallet
def get_pubkey(self, hex=True):
    return self.ecc.get_pubkey().encode('hex') if hex else self.ecc.get_pubkey()
 

# get the private key of the wallet
def get_privkey(self, hex=True):
    return self.ecc.get_privkey().encode('hex') if hex else self.ecc.get_privkey()


# method for signing a message
def sign(self, message):
    return self.ecc.sign(message).encode('hex')
 

# method for verifying a message
def verify(self, signature, message, public_key=None):
    if public_key is not None:
        return pyelliptic.ECC(curve='secp256k1', pubkey=public_key.decode('hex')).verify(signature.decode('hex'), message)
    return self.ecc.verify(signature, message)    


# get balance in the wallet
def get_balance(self, address):
    balance = 0
    for block in self.blocks:
        for transaction in block.transactions:
            if transaction["from"] == address:
                balance -= transaction["amount"]
            if transaction["to"] == address:
                balance += transaction["amount"]
    return balance


# create the transaction object
def create_transaction(self, to, amount):
    timestamp = datetime.datetime.utcnow().isoformat()
    signature = self.sign(
        self.generate_signable_transaction(
            self.get_pubkey(),
            to, 
            amount,
            timestamp))
    transaction = { 
        "from": self.get_pubkey(),
        "to": to, 
        "amount": amount,
        "signature": signature,
        "timestamp": timestamp,
        "hash": transaction_hash
    }   
    transaction["hash"] = self.calculate_transaction_hash(transaction)
    return self.broadcast_transaction(transaction)
 

# process the transaction
def calculate_transaction_hash(self, transaction):
    """ 
    Calculates sha-256 hash of transaction
 
    :param transaction: transaction
    :type transaction: dict(from, to, amount, timestamp, signature, (hash))
 
    :return: sha256 hash
    :rtype: str 
    """
    # pop hash so method can calculate transactions pre or post hash
    data = transaction.copy()
    data.pop("hash", None)
    data_json = json.dumps(data, sort_keys=True)
    hash_object = hashlib.sha256(data_json)
    return hash_object.hexdigest()
 

# make the transaction signable
def generate_signable_transaction(self, from_address, to_address, amount, timestamp):
    return ":".join((from_address, to_address, amount, timestamp))    


# notify everyone about this transaction
def broadcast_transaction(self, transaction):
    self.request_nodes_from_all()
    bad_nodes = set()
    data = {
        "transaction": transaction
    }
 
    for node in self.full_nodes:
        url = TRANSACTIONS_URL.format(node, FULL_NODE_PORT)
        try:
            response = requests.post(url, data)
        except requests.exceptions.RequestException as re:
            bad_nodes.add(node)
    for node in bad_nodes:
        self.remove_node(node)
    bad_nodes.clear()
    return