from src.blockchain import blockchain
from uuid import uuid4
from flask import Flask, jsonify, request

# instantiate the Flask node
app = Flask(__name__)

# generate unique address for our node
identifier = str(uuid4()).replace('-', '')


@app.route('/mine', methods=['GET'])
def mine():
    # run proof-of-work algorithm
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


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json(force=True)

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.reach_consensus()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200