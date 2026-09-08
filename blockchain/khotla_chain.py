import hashlib
import json
import time


class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }

        encoded = json.dumps(
            block_data,
            sort_keys=True
        ).encode()

        return hashlib.sha256(encoded).hexdigest()

    def mine(self, difficulty=3):
        target = "0" * difficulty

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()


class KhotlaChain:
    def __init__(self):
        self.difficulty = 3
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(
            index=0,
            transactions=[],
            previous_hash="0"
        )

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": time.time()
        }

        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return None

        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )

        new_block.mine(self.difficulty)

        self.chain.append(new_block)
        self.pending_transactions = []

        return new_block

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def get_balance(self, address):
        balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == address:
                    balance -= transaction["amount"]

                if transaction["receiver"] == address:
                    balance += transaction["amount"]

        return balance


if __name__ == "__main__":
    blockchain = KhotlaChain()

    blockchain.add_transaction(
        "KHT_GENESIS",
        "THABISO_WALLET",
        1000
    )

    block = blockchain.mine_pending_transactions()

    print("Khotla Chain started!")
    print("Block:", block.index)
    print("Hash:", block.hash)
    print("Chain valid:", blockchain.is_valid())
    print(
        "Thabiso wallet balance:",
        blockchain.get_balance("THABISO_WALLET"),
        "KHT"
    )
