import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_votes = []
        self.registered_voters = set()  
        self.voting_deadline = None  
        self.new_block(proof=100, previous_hash='1')  # Genesis block

    def set_voting_deadline(self, hours=24):
        """Set voting deadline in hours from now"""
        self.voting_deadline = time() + (hours * 3600)
        return self.voting_deadline

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'votes': self.current_votes,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_votes = []
        self.chain.append(block)
        return block

    def new_vote(self, voter, candidate):
        # Check if voting period has ended
        if self.voting_deadline and time() > self.voting_deadline:
            raise ValueError("Voting period has ended")
            
        # Check if voter already voted
        if voter in self.registered_voters:
            raise ValueError("Voter has already cast a vote")
            
        self.current_votes.append({
            'voter': voter,
            'candidate': candidate,
            'timestamp': time()
        })
        self.registered_voters.add(voter)
        return self.last_block['index'] + 1

    def get_vote_counts(self):
        """Count votes for each candidate across all blocks"""
        vote_counts = {}
        
        # Count votes in confirmed blocks
        for block in self.chain:
            for vote in block['votes']:
                candidate = vote['candidate']
                if candidate in vote_counts:
                    vote_counts[candidate] += 1
                else:
                    vote_counts[candidate] = 1
        
        # Count votes in pending votes
        for vote in self.current_votes:
            candidate = vote['candidate']
            if candidate in vote_counts:
                vote_counts[candidate] += 1
            else:
                vote_counts[candidate] = 1
                
        return vote_counts

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000" 