# Blockchain Voting System

A simple blockchain-based voting system that demonstrates the core concepts of blockchain technology: immutability, transparency, and decentralization.

## Features

- Submit votes for candidates
- Mine new blocks to confirm votes
- View the entire blockchain for transparency
- Secure hashing with SHA-256

## Requirements

- Python 3.6+
- Flask

## Installation

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the application:
```
python app.py
```

3. Open in your browser:
```
http://127.0.0.1:5000/
```

## How to Use

1. Enter your name and the candidate's name, then submit your vote
2. Mine a block to add your vote to the blockchain
3. View the blockchain to see all votes and blocks

## How It Works

- Each vote is temporarily stored in a pending votes list
- Mining a block adds all pending votes to the blockchain
- The proof-of-work algorithm ensures security
- Each block contains a reference to the previous block's hash, creating an immutable chain 