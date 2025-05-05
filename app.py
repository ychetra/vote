from flask import Flask, request, jsonify, render_template
from blockchain import Blockchain
from time import time
import sys
import requests

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    port = request.host.split(':')[1]  # Get current port
    other_port = '5000' if port == '5001' else '5001'  # Get other node's port
    return render_template('index.html', port=port, other_port=other_port)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    required = ['voter', 'candidate']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing fields'}), 400
    
    try:
        index = blockchain.new_vote(data['voter'], data['candidate'])
        # Notify other node
        port = request.host.split(':')[1]
        other_port = '5000' if port == '5001' else '5001'
        try:
            requests.post(f'http://localhost:{other_port}/sync_vote', json=data)
        except:
            pass  # If other node is not available, continue anyway
        return jsonify({'message': f'Vote will be added to Block {index}'}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@app.route('/sync_vote', methods=['POST'])
def sync_vote():
    data = request.get_json()
    try:
        blockchain.new_vote(data['voter'], data['candidate'])
        return jsonify({'message': 'Vote synced'}), 201
    except ValueError:
        return jsonify({'message': 'Vote already exists'}), 400

@app.route('/mine', methods=['GET'])
def mine():
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    block = blockchain.new_block(proof)
    
    # Notify other node about new block
    port = request.host.split(':')[1]
    other_port = '5000' if port == '5001' else '5001'
    try:
        requests.post(f'http://localhost:{other_port}/sync_block', json={'block': block})
    except:
        pass  # If other node is not available, continue anyway
    
    return jsonify({'message': 'New block mined', 'block': block})

@app.route('/sync_block', methods=['POST'])
def sync_block():
    data = request.get_json()
    blockchain.chain.append(data['block'])
    return jsonify({'message': 'Block synced'}), 201

@app.route('/chain', methods=['GET'])
def chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)})

@app.route('/set-deadline', methods=['POST'])
def set_deadline():
    data = request.get_json()
    hours = data.get('hours', 24)  # Default to 24 hours if not provided
    
    deadline = blockchain.set_voting_deadline(hours)
    deadline_time = time_readable(deadline)
    
    return jsonify({
        'message': f'Voting deadline set',
        'deadline': deadline,
        'deadline_readable': deadline_time
    })

@app.route('/get-deadline', methods=['GET'])
def get_deadline():
    if not blockchain.voting_deadline:
        return jsonify({'message': 'No deadline has been set'}), 404
    
    time_left = blockchain.voting_deadline - time()
    is_active = time_left > 0
    
    return jsonify({
        'deadline': blockchain.voting_deadline,
        'deadline_readable': time_readable(blockchain.voting_deadline),
        'time_left_seconds': max(0, time_left),
        'is_active': is_active
    })

@app.route('/votes/count', methods=['GET'])
def vote_count():
    counts = blockchain.get_vote_counts()
    return jsonify({
        'vote_counts': counts,
        'total_votes': sum(counts.values())
    })

def time_readable(timestamp):
    """Convert timestamp to human readable date/time"""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(port=port) 