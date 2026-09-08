import hashlib
import secrets


class KhotlaWallet:
    def __init__(self):
        self.private_key = secrets.token_hex(32)

        public_key_data = hashlib.sha256(
            self.private_key.encode()
        ).hexdigest()

        self.public_key = public_key_data

        address_data = hashlib.sha256(
            self.public_key.encode()
        ).hexdigest()

        self.address = "KHT" + address_data[:40]

    def get_wallet_info(self):
        return {
            "address": self.address,
            "public_key": self.public_key
        }

    def sign_transaction(self, transaction):
        data = (
            transaction["sender"]
            + transaction["receiver"]
            + str(transaction["amount"])
        )

        signature = hashlib.sha256(
            (data + self.private_key).encode()
        ).hexdigest()

        return signature


if __name__ == "__main__":
    wallet = KhotlaWallet()

    print("Khotla Wallet Created")
    print("----------------------")
    print("Address:", wallet.address)
    print("Public Key:", wallet.public_key)

    print()
    print("IMPORTANT:")
    print("Private keys must never be shared.")
